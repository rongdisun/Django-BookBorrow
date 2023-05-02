import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts

from comment.forms import CommentForm
from .models import *
from django.views.generic import *


# Create your views here.

def index(request):
    categories = BookCategory.objects.all()
    search = request.GET.get("search", None)
    book_cate = request.GET.get("book_cate", None)
    if search:
        books = Book.objects.filter(name__contains=search).all()
    else:
        books = Book.objects.all()
    if book_cate:
        books = Book.objects.filter(book_cate__cate_name=book_cate).all()
    carousel_books = CarouselBook.objects.all()
    return render(request, "book/index.html", locals())


@login_required
def book_borrow(request):
    res = {"Flag": False, "msg": None}
    pk = request.GET.get("pk")
    exist = BookBorrow.objects.filter(
        user=request.user,
        book_id=pk,
        borrow_status=1
    ).exists()
    if exist:
        res["Flag"] = True
        res["msg"] = "您正在阅读这本书，换本书看吧！"
        return JsonResponse(res)
    else:
        res["msg"] = "借阅成功"
        BookBorrow.objects.create(user=request.user, book_id=pk)
        return JsonResponse(res)


@login_required
def book_borrow_again(request, pk):
    BookBorrow.objects.create(user=request.user, book_id=pk)
    return redirect("book:book_borrow_log")


class BookBorrowLog(LoginRequiredMixin, ListView):
    template_name = "book/book_borrow_log.html"
    model = BookBorrow
    context_object_name = "object_list"
    # paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name", None)
        if name:
            return BookBorrow.objects.filter(book__name__contains=name, user=self.request.user).all()
        else:
            return BookBorrow.objects.filter(user=self.request.user).all()


def book_return(request, pk):
    BookBorrow.objects.filter(id=pk).update(borrow_status=2)
    return redirect("book:book_borrow_log")


class BookDetail(DetailView):
    template_name = "book/book_detail.html"
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentForm()
        context["comment_form"] = comment_form
        comments = self.object.band_object.all()
        context["comments"] = comments
        user_is_favorite = self.object.favorite_object.filter(user=self.request.user).first()
        context["user_is_favorite"] = user_is_favorite
        favorites = Favorite.objects.filter(favorite_object=self.object).count()
        context["favorites"] = favorites

        return context


class BookFavoriteList(LoginRequiredMixin, ListView):
    template_name = "book/book_favorite.html"
    model = Book
    context_object_name = "object_list"
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name", None)
        if name:
            return Book.objects.filter(name__contains=name)
        else:
            return Book.objects.filter(favorite_object__user=self.request.user).all()


def book_favorite_delete(request, pk):
    Favorite.objects.filter(user=request.user, favorite_object_id=pk).delete()
    return redirect("book:book_favorite_list")


@require_GET
@login_required
def post_favorite(request):
    object_id = request.GET.get("object")
    exist = Favorite.objects.filter(user=request.user, favorite_object_id=object_id).exists()
    if exist:
        Favorite.objects.filter(user=request.user, favorite_object_id=object_id).first().delete()
    else:
        Favorite(user=request.user, favorite_object_id=object_id).save()
    return HttpResponse("hello")


@login_required
def my_borrow_cate_pie(request):
    categories = BookCategory.objects.filter(
        book_category__book_borrow_book__user=request.user
    ).annotate(
        cate_count=Count("book_category__book_borrow_book")
    )
    data = [(cate.cate_name, cate.cate_count) for cate in categories]
    c = (
        Pie()
        .add("", data,
             radius="55%",
             center=['50%', '50%'],
             rosetype='radius'
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=True,
                font_size=24,
                formatter='{b}:{c}次',
            )
        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))


@login_required
def book_data_analysis_view(requests):
    return render(requests, "book/book_data_analysis.html")
