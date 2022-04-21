import os
from decimal import Decimal

import requests
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from django.db import models
from django.middleware.csrf import rotate_token
from django.urls import reverse
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField

from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app import settings
from app.data import ARRAY_GENDER, ARRAY_ARMED
from app.utils import Utils


class Methods_Emails:

    @classmethod
    def send_verification_email(cls, request, to, name, action_url):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                'email/email-confirmation.html',
                {
                    'name': name,
                    'contact_url': contact_url,
                    'confirm_url': action_url,
                }
            )
            send_mail(
                settings.EMAIL_VERIFICATION_SUBJECT,
                settings.EMAIL_VERIFICATION_MESSAGE,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                fail_silently=False,
                html_message=html_content,
            )
        except Exception as e:
            print('Mail Exception')
        return True

    @classmethod
    def send_reset_password_email(cls, request, to, name, action_url):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                'email/email-reset-password.html',
                {
                    'name': name,
                    'contact_url': contact_url,
                    'reset_url': action_url,
                }
            )
            send_mail(
                settings.EMAIL_PASSWORD_RESET_SUBJECT,
                settings.EMAIL_PASSWORD_RESET_MESSAGE,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                fail_silently=False,
                html_message=html_content,
            )
        except Exception as e:
            print('Mail Exception')
        return True

    @classmethod
    def send_info_email(cls, request, to, name, message):
        try:
            contact_url = settings.APP_CONSTANT_COMPANY_WEBSITE
            html_content = render_to_string(
                'email/email-info.html',
                {
                    'name': name,
                    'message': message,
                    'contact_url': contact_url,
                }
            )
            send_mail(
                settings.EMAIL_NOTIFICATION_SUBJECT,
                settings.EMAIL_NOTIFICATION_MESSAGE,
                settings.APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID,
                [to],
                fail_silently=False,
                html_message=html_content,
            )
            return False, 'Success'
        except Exception as e:
            print('Mail Exception')
            return True, str(e)
