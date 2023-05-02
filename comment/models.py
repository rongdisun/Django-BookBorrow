from django.db import models
from django.conf import settings
from book.models import Book as BandObject
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


class Comment(MPTTModel):
    content = RichTextField()
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children")

    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commenter",
        verbose_name="评论者"
    )

    reply = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="被评论者",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="reply")

    create_time = models.DateTimeField(
        verbose_name="创建时间",
        auto_now_add=True)

    last_mod_time = models.DateTimeField(
        verbose_name="修改时间",
        auto_now=True)

    band_object = models.ForeignKey(
        BandObject,
        verbose_name="评论绑定对象",
        on_delete=models.CASCADE,
        related_name="band_object")

    is_show = models.BooleanField(
        verbose_name="是否显示",
        default=True,
        blank=False,
        null=False)

    class MPTTMeta:
        order_insertion_by = ["create_time"]

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
