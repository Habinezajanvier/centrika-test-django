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
from app.models import Access_Permissions
from app.utils import Utils


class Methods_Access_Permissions:
    @classmethod
    def get_access_permissions(cls):
        access_permissions = Access_Permissions.objects.all()
        auth_permissions = {}
        counter = 0
        for access_permission in access_permissions:
            auth_permissions[counter] = access_permission.access_permission_name
            counter = counter + 1
        return auth_permissions
