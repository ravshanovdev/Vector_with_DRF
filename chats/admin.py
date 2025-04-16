from django.contrib import admin
from .models import ChatModel, UserProfileModel

admin.site.register([ChatModel, UserProfileModel])

