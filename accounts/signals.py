# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdditionalUserInfo
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_additional_info(sender, instance, created, **kwargs):
    if created:
        # Create the AdditionalUserInfo object when the User is created
        AdditionalUserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_additional_info(sender, instance, **kwargs):
    # Save the AdditionalUserInfo object when the User is saved (if it's already created)
    instance.additional_info.save()
