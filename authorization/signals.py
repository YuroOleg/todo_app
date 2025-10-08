from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from user_profile.models import Profile

@receiver(post_save, sender=User)
def profile_creator(sender, instance, created, **kwargs):
    """Signal for creating user profile"""
    if created:
        Profile.objects.create(user=instance)