from __future__ import print_function
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import time

#import sib_api_v3_sdk
#from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

#configuration = sib_api_v3_sdk.Configuration()
#configuration.api_key['api-key'] = settings.EMAIL_API_KEY
#api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_mail(to, template, context):
    subject = "from the Python SDK!"
    


def send_activation_email(request, email, code):
    context = {
        'subject': _('Profile activation'),
        'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def send_activation_change_email(request, email, code):
    context = {
        'subject': _('Change email'),
        'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'change_email', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': _('Restore password'),
        'uri': request.build_absolute_uri(
            reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'restore_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': _('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)
