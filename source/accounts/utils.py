from __future__ import print_function
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import time
from trycourier import Courier
import imghdr

from pprint import pprint


client = Courier(auth_token=settings.MAIL_TOKEN)

def send_mail_to(to, template, context):
    client.send
    resp = client.send_message(
        message={
            "to":{"email": to},
            "template": "AQSVE0FASKMVFXHQTFPW4AY4H3QK",
            "data": {
                "subject": context['subject'],
                "activation_url": context['uri'],
                "message": context['message'],
            },
        }
    )
    
    print(resp['requestId'])

def send_found_person(to,context):
    
    resp = client.send_message(
        message={
            "to": [{
                "email": to,
            },
                {
                    "email":settings.EMAIL_HOST_USER,
                }],
            "template": "QYFX3MF1JJMYBQQFBT7586NYJJEJ",
            "data": {
                "subject": context["subject"],
                "person_name": context["person_name"],
                "address": context["address"],
                "found_at": context["found_at"],
                "message_user": context["message_user"],
            },
        }  
    )
    

def send_activation_email(request, email, code):
    context = {
        'subject': 'Profile activation',
        'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
        'message': 'Click on the link below to complete your registration:',
    }

    send_mail_to(email, 'activate_profile', context)


def send_activation_change_email(request, email, code):
    context = {
        'subject':'Change email',
        'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
        'message': 'To change your current email address, please follow the link:',
    }

    send_mail_to(email, 'change_email', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': 'Restore password',
        'uri': request.build_absolute_uri(
            reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
        'message': 'You received this email because you requested a password reset for your user account. Please, go to the following page and choose a new password:',
    }

    send_mail_to(email, 'restore_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': 'Your username',
        'uri': username,
        'message': 'Your username is:',
    }

    send_mail_to(email, 'forgotten_username', context)
