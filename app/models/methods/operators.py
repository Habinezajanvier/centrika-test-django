import os
import json
import bcrypt
from decimal import Decimal

import requests
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MaxLengthValidator
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from django.db import models
from django.db.models import Q
from django.middleware.csrf import rotate_token
from django.urls import reverse
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField

from app import settings
from app.data import ARRAY_GENDER, ARRAY_ARMED
from app.models.operators import Operators
from app.models.operator_access_permissions import Operator_Access_Permissions
from app.utils import Utils


class Methods_Operators:

    @classmethod
    def format_view(cls, request, operator, model):
        model.operator_created_at = Utils.get_convert_datetime(model.operator_created_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.operator_updated_at = Utils.get_convert_datetime(model.operator_updated_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        try:
            operator = Operators.objects.get(
                pk=model.operator_created_by)
            model.operator_created_by = str(
                operator.operator_first_name) + ' ' + str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.operator_updated_by)
            model.operator_updated_by = str(
                operator.operator_first_name) + ' ' + str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        return model

    @classmethod
    def format_input(cls, request):
        return {
        }

    @classmethod
    def form_view(cls, request, operator, model):
        return {
            'email': model.operator_username,
            'name': str(model.operator_first_name)+' '+str(model.operator_last_name),
            'type': model.operator_type,
            'gender': model.operator_gender,
            'phone_number': model.operator_phone_number,
            'organization_id': model.operator_organization,
        }

    @classmethod
    def validate(cls, request, operator, model, new=False):
        return False, 'Success', model

    @classmethod
    def create(cls, request, operator, data, model=None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Operators()

        model.operator_auth_key = Operators.generate_unique_token(
            Operators, 'operator_auth_key')
        # model.operator_password = make_password(data['password'])
        password = bytes(data['password'], 'utf-8')
        salt = bcrypt.gensalt(rounds=13)
        hashed = bcrypt.hashpw(password, salt)
        model.operator_password = hashed

        # if 'type' in data:
        #     model.operator_type = data['type']
        # else:
        model.operator_type = 0
        if 'name' in data:
            model.operator_first_name = data['name']
        else:
            model.operator_first_name = ''
        model.operator_last_name = ''
        # if 'gender' in data:
        #     model.operator_gender = data['gender']
        # else:
        model.operator_gender = 0
        if 'phone_number' in data:
            model.operator_phone_number = data['phone_number']
        else:
            model.operator_phone_number = ''
        if 'email' in data:
            model.operator_username = model.operator_email_id = data['email']
        else:
            model.operator_username = model.operator_email_id = ''
        if 'organization' in data:
            model.operator_organization = data['organization']
        else:
            model.operator_organization = '0'

        model.operator_created_at = Utils.get_current_datetime_utc()
        model.operator_created_by = operator.operator_id
        model.operator_updated_at = Utils.get_current_datetime_utc()
        model.operator_updated_by = operator.operator_id
        model.operator_status = Operators.STATUS_UNVERIFIED
        model.save()
        return model

    @classmethod
    def update(cls, request, operator, data, model):
        data = json.dumps(data)
        data = json.loads(data)

        # if 'type' in data:
        #     model.operator_type = data['type']
        if 'name' in data:
            model.operator_first_name = data['name']
        # if 'gender' in data:
        #     model.operator_gender = data['gender']
        if 'phone_number' in data:
            model.operator_phone_number = data['phone_number']
        if 'email' in data:
            model.operator_email_id = data['email']
        if 'organization' in data:
            model.operator_organization = data['organization']

        model.operator_updated_at = Utils.get_current_datetime_utc()
        model.operator_updated_by = operator.operator_id
        model.save()
        return model

    @classmethod
    def update_status(cls, request, operator, model, status):
        model.operator_updated_at = Utils.get_current_datetime_utc()
        model.operator_updated_by = operator.operator_id
        model.operator_status = status
        model.save()
        return model

    @classmethod
    def delete(cls, request, model, operator):
        Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=model.operator_id).delete()
        model.delete()
        return True

    @classmethod
    def get_auth_permissions(cls, operator):
        operator_auth_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id)
        auth_permissions = {}
        counter = 0
        for operator_auth_permission in operator_auth_permissions:
            auth_permissions[counter] = operator_auth_permission.operator_access_permission_name
            counter = counter + 1
        return auth_permissions
