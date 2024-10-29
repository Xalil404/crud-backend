from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# for google authentication
from django.contrib.auth.signals import user_logged_in
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# for google authentication
@receiver(user_logged_in)
def create_auth_token(sender, user, request, **kwargs):
    if not Token.objects.filter(user=user).exists():
        Token.objects.create(user=user)
