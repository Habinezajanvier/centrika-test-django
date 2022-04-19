from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from decimal import Decimal

from app import settings
from app.data import ARRAY_GENDER


class Cards(models.Model):
    TITLE = settings.MODEL_CARDS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_CARDS_SINGULAR_TITLE
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

    card_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    card_type = models.IntegerField(
        'Type', blank=False, default=0)
    card_number = models.CharField(
        'Number', max_length=100, blank=False, unique=True)
    card_customer_id = models.IntegerField(
        'Customer', blank=False, default=0)
    card_balance = models.DecimalField('Balance', max_digits=30, decimal_places=2,
                                       default=Decimal(0.0))
    card_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    card_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    card_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    card_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    card_status = models.IntegerField(
        'Status', blank=False, default=STATUS_ACTIVE)

    class Meta:
        db_table = "cards"

    def __unicode__(self):
        return self.card_id
