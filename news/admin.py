from django.contrib import admin
from .models import (
    Post, 
    Author, 
    Category,
    Comment,
)

class CommentInLine(admin.TabularInline):
    model = Comment



class PostAdmin(admin.ModelAdmin):
    inlines = [
    CommentInLine,
    ]

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)