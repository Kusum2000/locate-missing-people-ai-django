import datetime
from distutils.command.upload import upload
from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from localflavor.in_.models import INStateField
from django.utils.translation import gettext as _
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/media/missing/')

class FileMissing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/')

    first_name = models.CharField(_('First name'),max_length=30, blank=True)
    last_name = models.CharField(_('Last name'),max_length=90, blank=True)
    dob = models.DateField(_('Date of Birth'),blank=True)
    date_of_missing = models.DateField(_('Date of Missing'))
    time_of_missing = models.TimeField(_('Time of Missing'))

    filed_at = models.DateTimeField(auto_now_add=True)

    street = models.CharField(_("Street"), max_length=128)
    area = models.CharField(_("Area"), max_length=128, blank=True)
    city = models.CharField(_("City"), max_length=64, default="Bangalore")
    state = INStateField(_("State"))
    zip_code = models.CharField(_("Pin code"),max_length=6 )


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

