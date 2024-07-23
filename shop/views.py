from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
import json 


# Create your views here.

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'Shop/index.html', {'products':products})




def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Success You can Login now..!')
            return redirect('/login')
    return render(request,'Shop/register.html', {'form':form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request, username=name,password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request,'logging in Successfully')
                return redirect('/')
            else:
                 messages.error(request, 'Invalid Credentials')
                 return redirect('/')
    return render(request, 'Shop/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'logged out Successfully')
        return redirect('/')  



def collections(request):
    category = Category.objects.filter(status=0)
    return render(request,'Shop/collections.html',{'category':category})


def collectionsview(request, name):
    if(Category.objects.filter(name=name , status=0)):
        products=Product.objects.filter(category__name=name)  #main  __
        return render(request , 'Shop/products/index.html' , {'products':products , "category__name":name})
    else:
        messages.warning(request , 'No such Category Found')
        return redirect('collections')
    
def product_details(request, Cname , Pname):
    if(Category.objects.filter(name=Cname , status=0)):
        if(Category.objects.filter(name=Pname , status=0)):
            products=Product.objects.filter(name=Pname , status=0).first()
            return render(request , 'Shop/products/product_details.html' , {'products':products})
        else:
            messages.warning(request , 'No such Category Found')
            return redirect('collections')
        
    else: 
        messages.warning(request , 'No such Category Found')
        return redirect('collections')   
    


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            product_qty=data['producy_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user, product_id=product_id):
                    return JsonResponse({'status':'Product Already Added in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user.id,product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status':'Product  Added in Cart'}, status=200)  
                    else:
                        return JsonResponse({'status':'Product Stock Not Avabilable'}, status=200)
            else:
                return JsonResponse({'status':'Login to Add Cart'}, status=200)      
        else:
            return JsonResponse({'status':'Invalid Access'}, status=200)   


def cart_page(request):
        if request.user.is_authenticated:
            cart=Cart.objects.filter(user=request.user)
            return render(request,'Shop/cart.html', {'cart':cart})
        else:
            return redirect ('/')
        
def remove_cart(request,cid):
    cartiteam=Cart.objects.get(id=cid)
    cartiteam.delete()
    return redirect('/cart')      


           
def add_fav_page(request):
     if request.user.is_authenticated:
         data=json.load(request)
         product_id=data['pid']
         product_status=Product.objects.get(id=product_id)
     
         if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status':'Product Already Added in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user.id,product_id=product_id)
                    return JsonResponse({'status':'Product  Added in Favourite'}, status=200)  
                   
         else:
             return JsonResponse({'status':'Login to Add Favourite'}, status=200)      
     else:
         return JsonResponse({'status':'Invalid Access'}, status=200)   


def favview_page(request):
        if request.user.is_authenticated:
            fav=Favourite.objects.filter(user=request.user)
            return render(request,'Shop/fav.html', {'fav':fav})
        else:
            return redirect ('/')
        
def remove_fav(request,fid):
    fav_item=Cart.objects.get(id=fid)
    fav_item.delete()
    return redirect('/fav')  
               
               
                      
    
        
        
