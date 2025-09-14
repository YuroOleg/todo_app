from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from user_profile.models import Profile

@receiver(post_save, sender=User)
def profile_saver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
