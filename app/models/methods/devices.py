from app.models.methods.vehicles import Methods_Vehicles
from app.models.vehicles import Vehicles
from app.models.stops import Stops
import json
from django.db import models
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils.safestring import mark_safe

from app import settings
from app.models import Devices, Operators
from app.utils import Utils


class Methods_Devices(models.Model):
    @classmethod
    def format_view(cls, request, operator, model):
        model.device_created_at = Utils.get_convert_datetime(model.device_created_at,
                                                             settings.TIME_ZONE,
                                                             settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.device_updated_at = Utils.get_convert_datetime(model.device_updated_at,
                                                             settings.TIME_ZONE,
                                                             settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.device_deployed_at = Utils.get_convert_datetime(model.device_deployed_at,
                                                              settings.TIME_ZONE,
                                                              settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

        try:
            operator = Operators.objects.get(
                pk=model.device_created_by)
            model.device_created_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.operator_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.device_updated_by)
            model.device_updated_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.operator_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.device_deployed_by)
            model.device_deployed_by = mark_safe(
                '<a href=' + reverse("operators_view",
                                     args=[operator.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(operator.operator_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        return model

    @classmethod
    def format_input(cls, request):
        serial_no = request.POST['serial_no'].upper()
        asis_serial_no = request.POST['asis_serial_no'].upper()
        return {
            'serial_no': serial_no,
            'asis_serial_no': asis_serial_no,
        }

    @classmethod
    def form_view(cls, request, operator, model, api=False):
        return {
            'id': model.device_id,
            'type': model.device_type,
            'serial_no': model.device_serial_no,
            'name': model.device_name,
            'vehicle_id': model.device_vehicle_id,
            'vehicle_code': model.device_vehicle_code,
            'asis_serial_no': model.device_asis_serial_no,
        }

    @classmethod
    def validate(cls, request, operator, model, new=False):
        # serial_no
        try:
            exists = Devices.objects.get(
                device_serial_no=model.device_serial_no)
        except(TypeError, ValueError, OverflowError, Devices.DoesNotExist):
            exists = None
        if exists is not None and exists.device_id != model.device_id:
            return True, 'Serial Number is already in use.', model

        # vehicle
        if model.device_vehicle_id != 0 and model.device_vehicle_id != '0':
            try:
                exists = Devices.objects.get(
                    device_vehicle_id=model.device_vehicle_id)
            except(TypeError, ValueError, OverflowError, Devices.DoesNotExist):
                exists = None
            if exists is not None and exists.device_id != model.device_id:
                return True, settings.MODEL_VEHICLES_SINGULAR_TITLE+' is already assigned to other device.', model

        # update auto columns
        try:
            exists = Vehicles.objects.get(pk=model.device_vehicle_id)
            model.device_vehicle_code = exists.vehicle_code
            Methods_Vehicles.update_device(request, operator, exists, model)
        except(TypeError, ValueError, OverflowError, Vehicles.DoesNotExist):
            exists = None
            model.device_vehicle_id = 0
            model.device_vehicle_code = ''

        return False, 'Success', model

    @classmethod
    def new(cls, request, operator, data, model=None):
        data = json.dumps(data)
        data = json.loads(data)
        if model is None:
            model = Devices()
            model.device_type = Devices.TYPE_NONE
        return False, 'Success', model

    @classmethod
    def create(cls, request, operator, data, model=None, status=None):
        data = json.dumps(data)
        data = json.loads(data)
        if model is None:
            model = Devices()
            model.device_type = Devices.TYPE_NONE

        if 'serial_no' in data:
            model.device_serial_no = data['serial_no']
        else:
            return True, 'Invalid Serial Number.', None

        if 'name' in data:
            model.device_name = data['name']
        else:
            return True, 'Invalid Name.', None

        if 'vehicle_id' in data:
            model.device_vehicle_id = data['vehicle_id']
        else:
            return True, 'Invalid '+settings.MODEL_VEHICLES_SINGULAR_TITLE+'.', None
        
        if 'asis_serial_no' in data:
            model.device_asis_serial_no = data['asis_serial_no']
        else:
            return True, 'Invalid ASIS Device Serial Number.', None

        # other fields
        if 'os' in data:
            model.device_os = data['os']
        else:
            model.device_os = ''
        if 'imei' in data:
            model.device_imei = data['imei']
        else:
            model.device_imei = ''
        if 'model' in data:
            model.device_model = data['model']
        else:
            model.device_model = ''
        if 'push_key' in data:
            model.device_push_key = data['push_key']
        else:
            model.device_push_key = ''
        if 'os' in data:
            model.device_app_version_code = data['version_code']
        else:
            model.device_app_version_code = 0
        if 'os' in data:
            model.device_app_version_name = data['version_name']
        else:
            model.device_app_version_name = ''

        model.device_created_at = Utils.get_current_datetime_utc()
        model.device_created_by = operator.operator_id
        model.device_updated_at = Utils.get_current_datetime_utc()
        model.device_updated_by = operator.operator_id
        model.device_deployed_at = Utils.get_current_datetime_utc()
        model.device_deployed_by = operator.operator_id

        if status is None:
            model.device_status = Devices.STATUS_INACTIVE
        else:
            model.device_status = status

        error, message, model = Methods_Devices.validate(
            request, operator, model, new=True)
        if error:
            return error, message, None
        model.save()
        return False, 'Success', model

    @classmethod
    def update(cls, request, operator, data, model, status=None):
        data = json.dumps(data)
        data = json.loads(data)

        if 'serial_no' in data:
            model.device_serial_no = data['serial_no']
        else:
            return True, 'Invalid Serial Number.', None

        if 'name' in data:
            model.device_name = data['name']
        else:
            return True, 'Invalid Name.', None

        if 'vehicle_id' in data:
            model.device_vehicle_id = data['vehicle_id']
        else:
            return True, 'Invalid '+settings.MODEL_VEHICLES_SINGULAR_TITLE+'.', None
        
        if 'asis_serial_no' in data:
            model.device_asis_serial_no = data['asis_serial_no']
        else:
            return True, 'Invalid ASIS Device Serial Number.', None

        # other fields
        if 'os' in data:
            model.device_os = data['os']
        if 'imei' in data:
            model.device_imei = data['imei']
        if 'model' in data:
            model.device_model = data['model']
        if 'push_key' in data:
            model.device_push_key = data['push_key']
        if 'os' in data:
            model.device_app_version_code = data['version_code']
        if 'os' in data:
            model.device_app_version_name = data['version_name']

        model.device_updated_at = Utils.get_current_datetime_utc()
        model.device_updated_by = operator.operator_id
        model.device_deployed_at = Utils.get_current_datetime_utc()
        model.device_deployed_by = operator.operator_id

        if status is not None:
            model.device_status = status

        error, message, model = Methods_Devices.validate(
            request, operator, model, new=True)
        if error:
            return error, message, None
        model.save()
        return False, 'Success', model

    @classmethod
    def update_status(cls, request, operator, model, status, action=None, data=None):
        model.device_updated_at = Utils.get_current_datetime_utc()
        model.device_updated_by = operator.operator_id
        model.device_status = status

        model.save()
        return model

    @classmethod
    def delete(cls, request, model, operator):
        model.delete()
        return True
