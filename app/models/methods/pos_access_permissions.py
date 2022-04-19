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
from app.models import Pos_Access_Permissions
from app.utils import Utils


class Methods_Pos_Access_Permissions:
    @classmethod
    def get_pos_access_permissions(cls):
        pos_access_permissions = Pos_Access_Permissions.objects.all()
        auth_permissions = {}
        counter = 0
        for pos_access_permission in pos_access_permissions:
            auth_permissions[counter] = pos_access_permission.pos_access_permission_name
            counter = counter + 1
        return auth_permissions
