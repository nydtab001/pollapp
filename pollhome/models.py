#from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vote(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    choice = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} has voted"


@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Vote.objects.create(user=instance)
