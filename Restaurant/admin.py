from django.contrib import admin
from .models import Restaurant

# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "addr",
        "longtitude",
        "latitude",
        "tel",
        "category",
        "image",
        "thumbnail",
        "imgurl",
        "description",
    )
    search_fields = (
        "title",
        "addr",
        "longtitude",
        "latitude",
        "tel",
        "category",
        "image",
        "thumbnail",
        "imgurl",
        "description",
    )


admin.site.register(Restaurant, RestaurantAdmin)
