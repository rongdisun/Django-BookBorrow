from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path("post-comment/<int:band_object_id>/", views.post_comment, name="post_comment"),
    path("post-comment/<int:band_object_id>/<int:parent_comment_id>", views.post_comment, name="reply_comment"),
]
