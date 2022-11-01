from django.shortcuts import render,redirect
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def index(request):

    return render(request, "Restaurant/index.html")

@login_required
def create(request):
    if request.method == 'POST':
        Restaurant_Form = RestaurantForm(request.POST, request.FILES)
        if Restaurant_Form.is_valid():
            restaurant = Restaurant_Form.save(commit=False)
            # 로그인한 유저 => 작성자네!
            restaurant.user = request.user 
            restaurant.save()
            #messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('Restaurant:index')
    else: 
        Restaurant_Form= RestaurantForm()
    context = {
        'Restaurant_Form': Restaurant_Form
    }
    return render(request, 'Restaurant/create.html', context=context)