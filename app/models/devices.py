from decimal import Decimal

from django.db import models
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare

from app import settings


class Devices(models.Model):
    TITLE = settings.MODEL_DEVICES_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_DEVICES_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TYPE_NONE = 'none'
    ARRAY_TYPE = [
        (TYPE_NONE.title()).replace('-', ' '),
    ]
    DROPDOWN_TYPE = (
        ('', '--select--'),
        (TYPE_NONE, (TYPE_NONE.title()).replace('-', ' ')),
    )

    TEXT_STATUS_ACTIVE = 'Active'
    TEXT_STATUS_INACTIVE = 'Inactive'
    TEXT_STATUS_BLOCKED = 'Blocked'
    STATUS_ACTIVE = 0
    STATUS_INACTIVE = 1
    STATUS_BLOCKED = 2
    ARRAY_STATUS = [
        STATUS_ACTIVE,
        STATUS_INACTIVE,
        STATUS_BLOCKED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_INACTIVE,
        TEXT_STATUS_BLOCKED,
    ]
    DROPDOWN_STATUS = (
        ('', '--select--'),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_INACTIVE, TEXT_STATUS_INACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Active <b></div>'
    HTML_TAG_STATUS_INACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_INACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Inactive <b></div>'
    HTML_TAG_STATUS_BLOCKED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Blocked <b></div>'

    device_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    device_type = models.CharField(
        'Type', max_length=10, blank=False, choices=DROPDOWN_TYPE, default=TYPE_NONE)
    device_serial_no = models.CharField(
        'Serial No.', max_length=255, blank=False, unique=True)

    device_name = models.CharField('Name', max_length=255, blank=True)

    # foreign keys
    device_vehicle_id = models.IntegerField('Vehicle', blank=False, default=0)
    device_vehicle_code = models.CharField(
        'Vehicle', max_length=255, blank=True)
    device_location_latitude = models.DecimalField('Location latitude', max_digits=30, decimal_places=6,
                                                   default=Decimal(0.0))
    device_location_longitude = models.DecimalField('Location longitude', max_digits=30, decimal_places=6,
                                                    default=Decimal(0.0))

    # app
    device_os = models.CharField('OS', max_length=255, blank=True)
    device_imei = models.CharField('IMEI', max_length=255, blank=True)
    device_model = models.CharField('Model', max_length=255, blank=True)
    device_push_key = models.CharField('Push Key', max_length=255, blank=True)
    device_app_version_code = models.IntegerField(
        'App Version Code', blank=False, default=0)
    device_app_version_name = models.CharField(
        'App Version Name', max_length=255, blank=True)

    # asis
    device_asis_serial_no = models.CharField(
        'ASIS Device Serial No.', max_length=255, blank=True)

    device_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    device_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    device_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    device_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    device_deployed_at = models.IntegerField(
        'Deployed At', blank=False, default=0)
    device_deployed_by = models.IntegerField(
        'Deployed By', blank=False, default=0)
    device_status = models.IntegerField(
        'Status', blank=False, default=STATUS_ACTIVE)

    def __unicode__(self):
        return self.device_id

    @classmethod
    def generate_unique_token(cls, attribute):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(32)
            if Devices.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token

    @classmethod
    def generate_random_number(cls, attribute, length):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(length, allowed_chars='0123456789')
            if (not token.startswith('0')) and Devices.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token
