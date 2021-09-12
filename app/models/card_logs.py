from decimal import Decimal
from django.db import models
from django.utils.crypto import get_random_string

from app import settings


class Card_Logs(models.Model):
    TITLE = settings.MODEL_CARDS_LOGS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_CARDS_LOGS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    card_log_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    card_log_card_number = models.CharField(
        'Card Number', max_length=255, blank=False)
    card_log_device_serial_number = models.CharField(
        'Device Serial No.', max_length=255, blank=False)
    card_log_institution_code = models.CharField(
        'Institution Code', max_length=255, blank=False)
    card_log_network_id = models.CharField(
        'Network Id', max_length=255, blank=False)

    card_log_login_request_body = models.TextField(
        'Start Session Request Body', blank=True)
    card_log_login_response = models.TextField(
        'Start Session Response', blank=True)

    card_log_start_session_request_body = models.TextField(
        'Start Session Request Body', blank=True)
    card_log_start_session_response = models.TextField(
        'Start Session Response', blank=True)

    card_log_get_purse_1_request_body = models.TextField(
        'Get Purse Request Body', blank=True)
    card_log_get_purse_1_response = models.TextField(
        'Get Purse Response', blank=True)

    card_log_web_top_up_request_body = models.TextField(
        'Web Top Up Request Body', blank=True)
    card_log_web_top_up_response = models.TextField(
        'Web Top Up Response', blank=True)

    card_log_get_purse_2_request_body = models.TextField(
        'Get Purse Request Body', blank=True)
    card_log_get_purse_2_response = models.TextField(
        'Get Purse Response', blank=True)

    card_log_end_session_request_body = models.TextField(
        'End Session Request Body', blank=True)
    card_log_end_session_response = models.TextField(
        'End Session Response', blank=True)

    card_log_amount = models.DecimalField('Amount', max_digits=30, decimal_places=2,
                                          default=Decimal(0.0))
    card_log_old_balance = models.DecimalField('Old Balance', max_digits=30, decimal_places=2,
                                               default=Decimal(0.0))
    card_log_new_balance = models.DecimalField('New Balance', max_digits=30, decimal_places=2,
                                               default=Decimal(0.0))
    card_log_response = models.TextField(
        'Response', blank=True)

    card_log_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    card_log_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    card_log_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    card_log_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)

    class Meta:
        db_table = "asis_card_logs"

    def __unicode__(self):
        return self.card_log_id

    @classmethod
    def generate_unique_token(cls, attribute):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(32)
            if Card_Logs.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token

    @classmethod
    def generate_random_number(cls, attribute, length):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(length, allowed_chars='0123456789')
            if (not token.startswith('0')) and Card_Logs.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token
