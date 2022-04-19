from app.models.cards import Cards
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from decimal import Decimal

from app import settings
from app.data import ARRAY_GENDER


class Card_Balance(models.Model):
    TITLE = settings.MODEL_CARD_BALANCE_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_CARD_BALANCE_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    card_balance_id = models.AutoField(
        SINGULAR_TITLE + ' Id', primary_key=True)
    card_balance_card_id = models.IntegerField(
        'Card', blank=False, default=0)
    card_balance_company_id = models.IntegerField(
        'Company', blank=False, default=0)
    card_balance_amount = models.DecimalField('Amount', max_digits=30, decimal_places=2,
                                              default=Decimal(0.0))
    card_balance_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    card_balance_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    card_balance_status = models.IntegerField(
        'Status', blank=False, default=Cards.STATUS_ACTIVE)

    class Meta:
        db_table = "card_balance"

    def __unicode__(self):
        return self.card_balance_id
