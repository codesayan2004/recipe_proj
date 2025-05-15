from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from .models import AdditionalUserInfo, FoodItem, Wishlist
# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        confirn_password = request.POST.get('confirm_password')
        # Perform validation checks here
        if (password != confirn_password):
            messages.info(request,"Password Do Not Match")
            return redirect('/register')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/register') 
        user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "User registered successfully")
        return redirect('/login')
    

    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Hii")
            messages.success(request, "Login successful")
            return redirect('/dashboard')
        else:
            messages.info(request, "Invalid credentials")
            return redirect('/login')

    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        template = loader.get_template('dashboard.html')
        context = {}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')
    
def profile(request):
    if request.user.is_authenticated:
        template = loader.get_template('profile.html')
        context = {"user": request.user}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')
    
def recipes(request):
    if request.user.is_authenticated:
        food_items = FoodItem.objects.all()
        template = loader.get_template('recipes.html')
        context = {'food_items': food_items}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')

def guest_recipes(request):
    food_items = FoodItem.objects.all()
    template = loader.get_template('recipes.html')
    context = {'food_items': food_items}
    return HttpResponse(template.render(context, request))

def particular_recipe(request, id):
    itm = FoodItem.objects.get(id=id)
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, recipe=itm).exists()
    template = loader.get_template("part_recipe.html")
    context = {
        'item' : itm,
        'in_wishlist': in_wishlist
    }
    return HttpResponse(template.render(context,request))

def add_recipe(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            short_desc = request.POST.get('short_desc')
            procedure = request.POST.get('procedure')
            image = request.FILES.get('image')
            food_item = FoodItem.objects.create(
                auth=request.user,
                title=title,
                short_desc=short_desc,
                procedure=procedure,
                image=image
            )
            food_item.save()
            # Update user's recipe count
            user_info = AdditionalUserInfo.objects.get(user=request.user)
            user_info.recipe_cnt += 1
            user_info.save()
            messages.success(request, "Recipe added successfully")
            return redirect('/dashboard/recipe/')
        template = loader.get_template('add_recipe.html')
        context = {}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')
    
def my_recipes(request):
    if request.user.is_authenticated:
        food_items = FoodItem.objects.filter(auth=request.user)
        template = loader.get_template('my_recipe.html')
        context = {'food_items': food_items}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')

def particular_my_recipe(request, id):
    itm = FoodItem.objects.get(id=id)
    template = loader.get_template("my_recipe_details.html")
    context = {
        'item' : itm
    }
    return HttpResponse(template.render(context,request))

def delete_recipe(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            food_item = FoodItem.objects.get(id=id)
            if food_item.auth != request.user:
                messages.error(request, "You are not authorized to delete this recipe")
                return redirect('/dashboard/my_recipes/')
            user_info = AdditionalUserInfo.objects.get(user=request.user)
            user_info.recipe_cnt -= 1
            user_info.save()
            food_item.delete()
            messages.success(request, "Recipe deleted successfully")
            return redirect('/dashboard/my_recipes/')
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')
    
def update_recipe(request, id):
    food_item = FoodItem.objects.get(id=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            short_desc = request.POST.get('short_desc')
            procedure = request.POST.get('procedure')
            image = request.FILES.get('image')
            food_item.title = title
            food_item.short_desc = short_desc
            food_item.procedure = procedure
            if image:
                food_item.image = image
            food_item.save()
            # Update user's recipe count
            messages.success(request, "Recipe updated successfully")
            return redirect('/dashboard/my_recipes/')
        template = loader.get_template('update_recipe.html')
        context = {'item': food_item}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')


def guest_particular_recipe(request, id):
    return HttpResponse("You Need to Login First to View this Recipe") 

def toggle_wishlist(request, id):
    if request.user.is_authenticated:
        food_item = FoodItem.objects.get(id=id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, recipe=food_item)

        user_info = AdditionalUserInfo.objects.get(user=request.user)

        if created:
            messages.success(request, "Recipe added to wishlist")
            user_info.wishlist_cnt += 1
            user_info.save()
        else:
            wishlist_item.delete()
            messages.success(request, "Recipe removed from wishlist")
            user_info.wishlist_cnt -= 1
            user_info.save()

        return redirect(f'/dashboard/recipe/{id}')
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')
    
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        print(wishlist_items)
        food_items = [item.recipe for item in wishlist_items]
        template = loader.get_template('wishlist.html')
        context = {'food_items': food_items}
        return HttpResponse(template.render(context, request))
    else:
        messages.info(request, "You need to login first")
        return redirect('/login')