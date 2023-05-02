from django import template
from book.models import Book, BookCategory
from django.db.models.aggregates import Count
import pytz
from datetime import datetime
register = template.Library()


@register.simple_tag
def get_all_category():

    return BookCategory.objects.annotate(num_books=Count("book_category"))

