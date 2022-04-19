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

from app import settings
from app.data import ARRAY_GENDER, ARRAY_ARMED
from app.utils import Utils
from app.models import Failed_Login


class Methods_Failed_Login:
    @classmethod
    def add(cls, failed_login_username, failed_login_password, failed_login_from, failed_login_ip_address,
            failed_login_status):
        failed_login = Failed_Login()
        failed_login.failed_login_username = failed_login_username
        failed_login.failed_login_password = failed_login_password
        failed_login.failed_login_from = failed_login_from
        failed_login.failed_login_ip_address = failed_login_ip_address
        failed_login.failed_login_attempted_at = Utils.get_current_datetime_utc()
        failed_login.failed_login_status = failed_login_status
        return failed_login.save('Added Failed Login')
