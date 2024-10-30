from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    note = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *arg, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(pre_save, sender=User)
def create_user_profile_pre(sender, instance, *args, **kwargs):
    print("Burası pre_save metodudur.")
    # email gönderebiliriz.