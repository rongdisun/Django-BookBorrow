from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Comment

admin.site.register(Comment, DraggableMPTTAdmin)
