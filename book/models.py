import uuid
from pathlib import Path

from django.urls import reverse
from ckeditor.fields import RichTextField

from user.models import *
from django.db import models


# Create your models here.

def book_thumbnail_path(instance, filename):  # 第一个参数，虽然没用显视用到，但是必须有
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return Path("book", filename)


def carousel_book_path(instance, filename):  # 第一个参数，虽然没用显视用到，但是必须有
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return Path("carousel", filename)


class BookCategory(models.Model):
    cate_name = models.CharField(verbose_name="分类名", max_length=255, unique=True)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now=True)

    def __str__(self):
        return self.cate_name

    class Meta:
        verbose_name = "图书分类"
        verbose_name_plural = verbose_name


class Book(models.Model):
    name = models.CharField(verbose_name="书名", max_length=255)
    isbn = models.CharField(verbose_name="标准书号", max_length=13, unique=True)
    thumbnail = models.FileField(verbose_name="缩略图", upload_to=book_thumbnail_path)
    author = models.CharField(verbose_name="作者", max_length=255)
    publish_house = models.CharField(verbose_name="出版社", max_length=255)
    publish_date = models.DateField(verbose_name="出版时间")
    price = models.FloatField(verbose_name="价格")
    pages = models.SmallIntegerField(verbose_name="页数")
    stock = models.SmallIntegerField(verbose_name="库存", default=0)
    add_date = models.DateField(verbose_name="添加时间")
    intro = models.TextField(verbose_name="图书简介")
    book_cate = models.ForeignKey(
        verbose_name="所属分类",
        to=BookCategory,
        related_name="book_category",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self, ):
        return reverse("book:book_detail", args=[self.pk])

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = verbose_name


class CarouselBook(models.Model):
    cover = models.FileField(
        verbose_name="轮播图",
        upload_to=carousel_book_path
    )
    book = models.ForeignKey(
        verbose_name="关联图书",
        to=Book,
        on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name="标题", max_length=255)
    describe = models.CharField(verbose_name="描述", max_length=255)
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "推荐图书"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]


class BookBorrow(models.Model):
    borrow_status_choice = (
        (1, "借阅中"),
        (2, "已归还")
    )
    user = models.ForeignKey(
        verbose_name="用户",
        to=User,
        related_name="book_borrow_user",
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        verbose_name="图书",
        to=Book,
        related_name="book_borrow_book",
        on_delete=models.CASCADE
    )
    borrow_time = models.DateTimeField(verbose_name="借阅时间", auto_now=True)
    borrow_status = models.SmallIntegerField(
        verbose_name="借阅状态",
        choices=borrow_status_choice,
        default=1
    )


# 收藏的图书
class Favorite(models.Model):
    user = models.ForeignKey(
        verbose_name="收藏用户",
        to=User,
        related_name="favorite_user",
        on_delete=models.CASCADE
    )
    favorite_object = models.ForeignKey(
        verbose_name="收藏对象",
        to=Book,
        related_name="favorite_object",
        on_delete=models.CASCADE
    )
    create_time = models.DateTimeField(verbose_name="收藏时间", auto_now=True)
