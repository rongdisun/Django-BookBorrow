from django.urls import path
from .views import *

app_name = "book"

urlpatterns = [
    path("", index, name="index"),
    path("book_borrow/", book_borrow, name="book_borrow"),
    path("book_borrow_log/", BookBorrowLog.as_view(), name="book_borrow_log"),
    path("book_return/<pk>", book_return, name="book_return"),
    path("book_borrow_again/<pk>", book_borrow_again, name="book_borrow_again"),
    path("book_detail/<pk>", BookDetail.as_view(), name="book_detail"),

    path("book_favorite_list/", BookFavoriteList.as_view(), name="book_favorite_list"),
    path("book_favorite_delete/<pk>", book_favorite_delete, name="book_favorite_delete"),
    path("post_favorite/", post_favorite, name="post_favorite"),

    path("book_data_analysis_view/", book_data_analysis_view, name="book_data_analysis_view"),
    path("my_borrow_cate_pie/", my_borrow_cate_pie, name="my_borrow_cate_pie"),

]
