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
    STATUS=(
        ('Not found', 'Not found'),
        ('Found', 'Found')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img_id = models.CharField(max_length=100,null=True)
    img = models.ImageField(upload_to='missing/',null=True,blank=False)

    first_name = models.CharField(_('First name'),max_length=30, blank=False)
    last_name = models.CharField(_('Last name'),max_length=90, blank=False)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(_('Sex'),max_length=6, choices=GENDER_CHOICES,blank=False)
    dob = models.DateField(blank=False)
    date_of_missing = models.DateField(_('Date of Missing'),blank=False)
    time_of_missing = models.TimeField(_('Time of Missing'),blank=False)

    filed_at = models.DateTimeField(null=True,auto_now_add=True)

    extra_info = models.TextField(_("Addition Info"),max_length=200, blank=False)
    street = models.CharField(_("Street"), max_length=128,blank=False)
    area = models.CharField(_("Area"), max_length=128,blank=False)
    city = models.CharField(_("City"), max_length=64, default="Bangalore",blank=False)
    state = INStateField(_("State"),blank=False)
    zip_code = models.CharField(_("Pin code"),max_length=6,blank=False )
    status = models.CharField(max_length=20, null=True, choices=STATUS, default='Not found')


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

