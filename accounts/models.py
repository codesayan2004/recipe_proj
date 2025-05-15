# accounts/models.py
from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import User

class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional_info')
    recipe_cnt = models.IntegerField(default=0)
    wishlist_cnt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Info"
    
from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)  # Auth_ID (linked to Django User)
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=500)
    procedure = models.TextField()
    image = models.ImageField(upload_to='food_images/')

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  # use your Recipe model

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"