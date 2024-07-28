from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "photo",
        "created_at",
        "is_published",
        "views",
    )
    search_fields = ("name", "is_published")
