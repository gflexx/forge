from django.contrib import admin
from django.contrib.admin import AdminSite
from django.conf import settings

from .models import *

name = settings.SITE_NAME

AdminSite.site_title = f'{name}'
AdminSite.site_header = f'{name} Admin Panel'

admin.site.register(User)
admin.site.register(Profile)