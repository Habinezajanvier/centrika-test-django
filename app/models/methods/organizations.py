import json

from app import settings
from app.models.organizations import Organizations
from app.utils import Utils
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe


class Methods_Organizations:

    @classmethod
    def format_view(cls, request, operator, model):
        model.organization_created_at = Utils.get_convert_datetime(model.organization_created_at,
                                                                   settings.TIME_ZONE,
                                                                   settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.organization_updated_at = Utils.get_convert_datetime(model.organization_updated_at,
                                                                   settings.TIME_ZONE,
                                                                   settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        try:
            operator = Organizations.objects.get(
                pk=model.organization_created_by)
            model.organization_created_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.organization_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('')

        try:
            operator = Organizations.objects.get(
                pk=model.organization_updated_by)
            model.organization_updated_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.organization_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            print('')

        return model

    @classmethod
    def format_input(cls, request):
        return {
        }

    @classmethod
    def form_view(cls, request, operator, model):
        return {
            'name': model.organization_name,
            'email': model.organization_email_id,
            'phone_number': model.organization_phone_number,
        }

    @classmethod
    def validate(cls, request, operator, model, new=False):
        return False, 'Success', model

    @classmethod
    def create(cls, request, operator, data, model=None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Organizations()

        if 'name' in data:
            model.organization_name = str(data['name']).lower()
        else:
            model.organization_name = ''
        if 'email' in data:
            model.organization_email_id = data['email']
        else:
            model.organization_email_id = ''
        if 'phone_number' in data:
            model.organization_phone_number = data['phone_number']
        else:
            model.organization_phone_number = ''

        model.organization_created_at = Utils.get_current_datetime_utc()
        model.organization_created_by = operator.operator_id
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = operator.operator_id
        model.organization_status = Organizations.STATUS_ACTIVE
        model.save()
        return model

    @classmethod
    def update(cls, request, operator, data, model):
        data = json.dumps(data)
        data = json.loads(data)

        if 'name' in data:
            model.organization_name = str(data['name']).lower()
        if 'email' in data:
            model.organization_email_id = data['email']
        if 'phone_number' in data:
            model.organization_phone_number = data['phone_number']

        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = operator.operator_id
        model.save()
        return model

    @classmethod
    def update_status(cls, request, operator, model, status):
        model.organization_updated_at = Utils.get_current_datetime_utc()
        model.organization_updated_by = operator.operator_id
        model.organization_status = status
        model.save()
        return model

    @classmethod
    def delete(cls, request, model, operator):
        model.delete()
        return True