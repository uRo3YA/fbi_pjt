from django.contrib import admin
from .models import Review, Comment

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "created_at",
        "updated_at",
        "image",
        "Restaurant",
    )
    search_fields = (
        "title",
        "content",
        "created_at",
        "updated_at",
        "image",
        "Restaurant",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "user",
        "content",
        "created",
        "deleted",
        "reply",
    )
    search_fields = (
        "review",
        "user",
        "content",
        "created",
        "deleted",
        "reply",
    )


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
