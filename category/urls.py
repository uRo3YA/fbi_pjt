from django.urls import path
from . import views
from reviews import views as v2
# app_name과 path 이름으로

app_name = "category"

urlpatterns = [
   path("", views.index, name="index"),
   #path('', views.AllListView.as_view(), name='all_list'),

]