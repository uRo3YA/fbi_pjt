from django.urls import path
from . import views

# app_name과 path 이름으로

app_name = "Restaurant"

urlpatterns = [
   path("", views.index, name="index"),
   path("create/", views.create, name="create"),
]
