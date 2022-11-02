from django.urls import path
from . import views

# app_name과 path 이름으로

app_name = "reviews"

urlpatterns = [
   path("", views.index, name="index"),
   #path('create/', views.create, name='create'),
   path('<int:pk>/', views.detail, name='detail'),
   path('<int:pk>/update/', views.update, name='update'),
   path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
   path('<int:pk>/like/', views.like, name='like'),
   
   path("<int:pk>/create/", views.review_create, name="review_create"),
   path("<int:pk>/detail/<int:review_pk>", views.review_detail, name="review_create"),
]

