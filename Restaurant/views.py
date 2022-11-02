from django.shortcuts import render,redirect
from .models import Restaurant
from reviews.models import Review 
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView
def index(request):
    contents = Restaurant.objects.all()
    context = {
        "contents": contents,
    }
    return render(request, "Restaurant/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        Restaurant_Form = RestaurantForm(request.POST, request.FILES)
        if Restaurant_Form.is_valid():
            restaurant = Restaurant_Form.save(commit=False)           
            restaurant.save()
            return redirect('Restaurant:index')
    else: 
        Restaurant_Form= RestaurantForm()
    context = {
        'Restaurant_Form': Restaurant_Form
    }
    return render(request, 'Restaurant/create.html', context=context)

def detail(request, pk):
    info = Restaurant.objects.get(pk=pk)
    review = Review.objects.filter(Restaurant_id=info.pk)
    context = {
        "info": info,
        "reviews": review,
    }
    return render(request, "Restaurant/detail.html", context)

#관리자 권한으로 바꿔줘야함
@login_required
def update(request, pk):
    info = Restaurant.objects.get(pk=pk)
    if request.method == "POST":
        Restaurant_Form = RestaurantForm(request.POST, instance=info)
        if Restaurant_Form.is_valid():
            Restaurant_Form.save()
            return redirect("Restaurant:detail", info.pk)
    else:
        Restaurant_Form = RestaurantForm(instance=info)
    context = {
        "Restaurant_Form": Restaurant_Form,
    }
    return render(request, "Restaurant/update.html", context)

#관리자 권한으로 바꿔줘야함
@login_required
def delete(request, pk):
    info = Restaurant.objects.get(pk=pk)
    info.delete()
    return redirect('Restaurant:index')

