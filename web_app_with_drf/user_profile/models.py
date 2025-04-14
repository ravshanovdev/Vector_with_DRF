from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(max_length=13)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    follows = models.ManyToManyField(User, related_name='followed_by', symmetrical=False, blank=True)
    bio = models.TextField()
    twitter_link = models.CharField(max_length=155, blank=True, null=True)
    instagram_link = models.CharField(max_length=155, blank=True, null=True)
    facebook_link = models.CharField(max_length=155, blank=True, null=True)
    telegram_link = models.CharField(max_length=155, blank=True, null=True)
    pinterest_link = models.CharField(max_length=155, blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'userprofile'):
            user_profile = UserProfile(user=instance)
            user_profile.save()
            user_profile.follows.set([instance.id])
            user_profile.save()


post_save.connect(create_profile, sender=User)
