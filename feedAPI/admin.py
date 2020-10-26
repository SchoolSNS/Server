from django.contrib import admin
from .models import Comment, Post, Image, CommentImage, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(CommentImage)
admin.site.register(Like)