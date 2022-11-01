from django.urls import path
from . import views
from reviews import views as v2
# app_name과 path 이름으로

app_name = "Restaurant"

urlpatterns = [
   path("", views.index, name="index"),
   #path('', views.AllListView.as_view(), name='all_list'),
   path("create/", views.create, name="create"),
   path("<int:pk>/", views.detail, name="detail"),
   path('<int:pk>/create', v2.review_create, name="review_create"),
]
