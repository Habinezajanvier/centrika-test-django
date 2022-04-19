from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from decimal import Decimal

from app import settings
from app.data import ARRAY_GENDER


class Companies(models.Model):
    TITLE = settings.MODEL_COMPANIES_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_COMPANIES_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_STATUS_ACTIVE = 'Active'
    TEXT_STATUS_BLOCKED = 'Blocked'
    STATUS_ACTIVE = 1
    STATUS_BLOCKED = 0
    ARRAY_STATUS = [
        STATUS_ACTIVE,
        STATUS_BLOCKED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_BLOCKED,
    ]
    DROPDOWN_STATUS = (
        ('', '--select--'),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Active <b></div>'
    HTML_TAG_STATUS_BLOCKED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Blocked <b></div>'

    company_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    company_name = models.CharField(
        'Name', max_length=100, blank=False, unique=True)
    company_email_id = models.EmailField(
        'Email id', max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+250123456789'. Up to 13 digits allowed.")
    company_phone_number = models.CharField('Phone Number',
                                            validators=[phone_regex, MinLengthValidator(10),
                                                        MaxLengthValidator(13)],
                                            max_length=13, blank=True)
    company_logo_image = models.CharField(
        'Logo', max_length=255, blank=True)
    company_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    company_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    company_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    company_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    company_status = models.IntegerField(
        'Status', blank=False, default=STATUS_ACTIVE)

    class Meta:
        db_table = "companies"

    def __unicode__(self):
        return self.company_id
