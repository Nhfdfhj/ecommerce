from codecs import register
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from .models import Product, Contact, UserProduct , ProductHome
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from shop.models import Product
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="handleLogin")
def my_cart(request):
    user = request.user
    user_courses = UserProduct.objects.filter(user=user)
    context = {
        "user_courses":user_courses
    }
    return render(request=request, template_name="shop/my_cart.html",context= context)
    
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def home(request):
    allProds=[]
    product = ProductHome.objects.values('desc', 'image','product_name','price','subcategory')
    cats = {item['subcategory'] for item in product}
    for cat in cats:
        prod = ProductHome.objects.filter(subcategory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    context = {
        "allProds":allProds
    }
    return render(request, 'shop/home.html',context=context)

def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})



def producthomeView(request, product_name):
    product = ProductHome.objects.filter(id=product_name)
    return render(request, 'shop/prodView.html', {'product':product[0]})

def checkouthome(request,product_name):
    products = ProductHome.objects.filter(id=product_name)
    user = request.user
    if not request.user.is_authenticated:
        return redirect("handleLogin")
    
    #action = request.GET.get('action')
    #order = None
    #if action == 'create_payment':
    #    print("Creating Order Object")
    #    order = "Order Created"
    userProduct = UserProduct(user=user,product= products)
    userProduct.save()
    messages.success(request, " Your item has been successfully added to cart")
    context = {
        "product":products,
        #"order":order
    }
   
    return redirect('ShopHome')

def delete(request,myid):
    products = UserProduct.objects.get(id=myid)
   # user = request.user
   # userProduct = UserProduct(user=user,product= products)
    products.delete()
    messages.success(request, " Your item has been successfully removed from your cart")
    return redirect('my_cart')


def checkout(request,myid):
    products = Product.objects.get(id=myid)
    user = request.user
    if not request.user.is_authenticated:
        return redirect("handleLogin")
    
    #action = request.GET.get('action')
    #order = None
    #if action == 'create_payment':
    #    print("Creating Order Object")
    #    order = "Order Created"
    userProduct = UserProduct(user=user,product= products)
    userProduct.save()
    messages.success(request, " Your item has been successfully added to cart")
    context = {
        "product":products,
        #"order":order
    }
   
    return redirect('ShopHome')

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        messages.warning(request, "No search results found. Please refine your query.")
    return render(request, 'shop/search.html', params)

def handeSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            messages.warning(request," Your user name must be under 10 characters")
            return redirect("ShopHome")

        if not username.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return redirect("ShopHome")
        
        if (pass1!= pass2):
             messages.warning(request, " Passwords do not match")
             return redirect("ShopHome")
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect("Home")

    else:
        return HttpResponse("404 - Not found")
    
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("Home")

    
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("Home")
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return redirect("Home")
    messages.warning(request, "You are not login")

    return redirect("Home")