from django.shortcuts import render,redirect,get_object_or_404
from .models import Restaurant
from reviews.models import Review
from users.models import User 
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator
import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from urllib.request import urlopen as url_open
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json





def get_geo(addr):
    #naver map api key
    client_id = 'ureszraal9';    # 본인이 할당받은 ID 입력
    client_pw = 'mM198tK1l9K1yvDiLT315g8IWY5bogukDngUNxDF';    # 본인이 할당받은 Secret 입력

    api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='
    geo_coordi = {}
    add_urlenc = parse.quote(addr)  
    url = api_url + add_urlenc 
    
    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_pw)
    context=0
    try:
        response = url_open(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)   # json
            if response_body['addresses'] == [] :
                print("'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                print("Success!")
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None

    geo_coordi={"longtitude" : longitude,
            "latitude" : latitude}
    print(geo_coordi)
    return geo_coordi



def index(request):
    contents = Restaurant.objects.all()
    #contents = Store.objects.all()
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
            #print(restaurant.addr)
            result=get_geo(restaurant.addr)
            #print("longtitude:",result["longtitude"])
            #print("latitude:",result["latitude"])
            restaurant.longtitude=float(result["longtitude"])
            restaurant.latitude=float(result["latitude"])
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
    #store= Store.objects.get(pk=pk)
    review = Review.objects.filter(Restaurant_id=info.pk)
    #print(review.comment_set.all().count)
    storedict = {
        'lat': info.latitude,
        'lon': info.longtitude,
    }
    storeJson = json.dumps(storedict)
    context = {
        "info": info,
        "reviews": review,
        "store":info,
        'storeJson': storeJson
    }
    return render(request, "Restaurant/detail.html", context)

#관리자 권한으로 바꿔줘야함
@login_required
def update(request, pk):
    info = Restaurant.objects.get(pk=pk)
    if request.method == "POST":
        Restaurant_Form = RestaurantForm(request.POST,  request.FILES,instance=info)
        if Restaurant_Form.is_valid():
            result=get_geo(info.addr)
            #print("longtitude:",result["longtitude"])
            #print("latitude:",result["latitude"])
            info.longtitude=float(result["longtitude"])
            info.latitude=float(result["latitude"])
            info.save()
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

def search(request):
    result = Restaurant.objects.all().order_by('-id')
    q = request.POST.get('q', "") 
    if q:
        result = result.filter(title__icontains=q)
        return render(request, 'Restaurant/search.html', {'result' : result, 'q' : q})
    
    else:
        return render(request, 'Restaurant/search.html')

def map(request):
    return render(request, 'Restaurant/map.html')

def wishlist(request, pk):
    #user = request.user
    #user = get_user_model().objects.get(pk=request.user)
    #print(request.user.id)
    person=User.objects.get(pk=request.user.id)
    info =get_object_or_404( Restaurant, pk=pk)
    if request.user in info.wishlist.all(): 
        info.wishlist.remove(request.user)
        person.user_wishlist.remove(info.pk)
        is_liked = False
    else:
        info.wishlist.add(request.user)
        person.user_wishlist.add(info.pk)
        is_liked = True
    context = {'isLiked': is_liked, 'likeCount': info.wishlist.count()}
    return JsonResponse(context)

