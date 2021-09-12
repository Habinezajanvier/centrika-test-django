import json

from app import settings
from app.models.operator_access_permissions import Operator_Access_Permissions
from app.models.operators import Operators
from app.utils import Utils
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.safestring import mark_safe


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
            model.operator_created_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.operator_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.operator_updated_by)
            model.operator_updated_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.operator_name) + '</a>')
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
            'name': model.operator_name,
            'phone_number': model.operator_contact_phone_number,
            'organization_id': model.operator_organization_id,
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
            model.operator_type = Operators.TYPE_OTHER
            model.operator_gender = ''

        model.operator_auth_key = Operators.generate_unique_token(
            Operators, 'operator_auth_key')
        model.operator_password_hash = make_password(
            data['password'])

        if 'name' in data:
            model.operator_name = data['name']
        else:
            model.operator_name = ''
        if 'phone_number' in data:
            model.operator_contact_phone_number = data['phone_number']
        else:
            model.operator_contact_phone_number = ''
        if 'email' in data:
            model.operator_username = model.operator_contact_email_id = data['email']
        else:
            model.operator_username = model.operator_contact_email_id = ''
        if 'organization_id' in data:
            model.operator_organization_id = data['organization_id']
        else:
            model.operator_organization_id = 0

        model.operator_password_reset_token = ''
        model.operator_profile_photo_file_path = ''

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

        if 'name' in data:
            model.operator_name = data['name']
        if 'phone_number' in data:
            model.operator_contact_phone_number = data['phone_number']
        if 'email' in data:
            model.operator_contact_email_id = data['email']
        if 'organization_id' in data:
            model.operator_organization_id = data['organization_id']

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
            operators_operator_id_id=model.operator_id).delete()
        if model.operator_profile_photo_file_path:
            Utils.delete_file(model.operator_profile_photo_file_path.path)
        model.delete()
        return True

    @classmethod
    def get_auth_permissions(cls, operator):
        operator_auth_permissions = Operator_Access_Permissions.objects.filter(
            operators_operator_id_id=operator.operator_id)
        auth_permissions = {}
        counter = 0
        for operator_auth_permission in operator_auth_permissions:
            auth_permissions[counter] = operator_auth_permission.access_permissions_access_permission_name_id
            counter = counter + 1
        return auth_permissions
