from django.urls import path
from accounts.views import *

urlpatterns = [
    path('', home, name='home'),
    path('guest/', guest_recipes, name='guest'),
    path('guest/<int:id>/', guest_particular_recipe),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/add_recipe/', add_recipe, name='add_recipe'),
    path('dashboard/profile/', profile, name='profile'),
    path('dashboard/recipe/', recipes ,name='recipe'),
    path('dashboard/recipe/<int:id>/', particular_recipe, name='particular_recipe'),
    path('dashboard/my_recipes/', my_recipes, name='my_recipes'),
    path('dashboard/my_recipes/<int:id>/', particular_my_recipe, name='particular_my_recipe'),
    path('dashboard/update_recipe/<int:id>/', update_recipe, name='update_recipe'),
    path('dashboard/delete_recipe/<int:id>/', delete_recipe, name='delete_recipe'),
    path('wishlist/toggle/<int:id>/', toggle_wishlist, name='toggle_wishlist'),
    path('dashboard/wishlist/', wishlist, name='wishlist'),
]