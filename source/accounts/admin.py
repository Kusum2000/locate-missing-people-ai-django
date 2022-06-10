from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import FileMissing, Found, Activation



admin.site.register(FileMissing)
admin.site.register(Found)
admin.site.register(Activation)