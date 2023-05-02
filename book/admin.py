from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['cate_name', 'add_time']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'isbn', 'author', 'publish_house', 'price']


@admin.register(CarouselBook)
class CarouselBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'cover', 'add_time']
