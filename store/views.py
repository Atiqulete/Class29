from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,changePasswordForm,UserInfoForm
from django import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.db.models import Q
###########
import json
from cart.cart import Cart



def search(request):
    if request.method == "POST":
        search_term = request.POST.get('searched', '')  # Get the search term from the form

        # Perform the search query on the Product model
        products = Product.objects.filter(Q(name__icontains=search_term) | Q(price__icontains=search_term) | Q(descripton__icontains=search_term))

        if not products:  # If no results are found
            messages.info(request, "Sorry, no products match your search.")
            return render(request, 'search.html', {'searched': search_term, 'products': products})

        # If products are found, return the search term and results
        return render(request, 'search.html', {'searched': search_term, 'products': products})

    # If it's a GET request, just render the search page without results
    return render(request, 'search.html', {})

# def search(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         searched = Product.objects.filter(Q(name__icontains=searched) | Q(price__icontains=searched))
#         if not searched:
#             messages.success(request, "sorry you have no search")
#             return render(request,'search.html',{})
#         else:
#             return render(request,'search.html',{'searched':searched})
#     else:
#         return render(request,'search.html',{})

def update_info(request):
    if request.user.is_authenticated:
        # Use request.user directly
        current_profile = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been updated successfully!!!")
            return redirect('home')
        return render(request, 'update_info.html',{'form':form})
    else:
        messages.success(request, "Please correct the errors below!!!")
        return redirect('home')

@login_required
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = changePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated. Please log in again!")
                return redirect('login')  # Redirect to login page after updating the password
            else:
                # Display all form errors without redirecting
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                
                # Re-render the form with errors
                return render(request, 'update_password.html', {'form': form})
        else:
            form = changePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')  # Redirect to the home page if not authenticated

@login_required
def update_user(request):
    if request.user.is_authenticated:
        # Use request.user directly
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request, "User Has been Update!!!")
            return redirect('home')
        return render(request, 'update_user.html',{'user_form':user_form})
    else:
        messages.success(request, "You Must be Logged in to access that page!!!")
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category_summary(request):
    categories = Category.objects.all() 
    return render(request,'category_summary.html',{"categories":categories})

def category(request,foo):
    # Replace Hyphens with space
    foo = foo.replace('-','')
    # Grap the catagory from the url
    try:
        #look Up The Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category })
    
    except:
        messages.success(request,("That Category Doest't exit....!"))
        return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            
            #####################################
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
                
            
            #####################################
            messages.success(request,("you have been logged in !"))
            return redirect('home')
        else:
            messages.success(request,("there was an error, please try again !"))
            return redirect('login')
    else:
        
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out... Thanks"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("Username Created - Please Out Your User Info Below!"))
            return redirect('update_info')
        else:
            messages.success(request, ("Whoops! there was a problem registering ,Please try again!"))
            return redirect('register')

    return render(request,'register.html',{'form':form})
