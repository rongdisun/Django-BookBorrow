from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Comment
from book.models import Book as BandObject
from .forms import CommentForm


@require_POST
@login_required
def post_comment(request, band_object_id, parent_comment_id=None):
    band_object = get_object_or_404(BandObject, id=band_object_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.band_object = band_object
        new_comment.commenter = request.user

        # 二级回复
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)
            # 如果超过二级评论，就把他置为二级评论
            new_comment.parent_id = parent_comment.get_root().id
            # 被回复人
            new_comment.reply = parent_comment.commenter
            new_comment.save()
            redirect_url = band_object.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)

        new_comment.save()
        # 由于评论的数目在不断增加，所以要不断生成新的前端代码块，因此需要定位到锚点可以
        redirect_url = band_object.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
        return redirect(redirect_url)
    else:
        return HttpResponse("表单内容有误，请重新填写。")



