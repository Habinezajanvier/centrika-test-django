from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.middleware.csrf import rotate_token
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare
from decimal import Decimal

from app import settings
from app.data import ARRAY_GENDER


class Tickets_External(models.Model):
    TITLE = settings.MODEL_TICKETS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_TICKETS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    ticket_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    ticket_external = models.CharField('Organization', max_length=255, blank=False, default='')
    ticket_reference = models.CharField('Reference Ticket Id', max_length=255, blank=False, default='')
    ticket_company_name = models.CharField('Company', max_length=255, blank=False, default='')
    ticket_company_branch_name = models.CharField('Branch', max_length=255, blank=False, default='')
    ticket_agent_name = models.CharField('Agent', max_length=255, blank=False, default='')
    ticket_route_name = models.CharField('Bus Route', max_length=255, blank=False, default='')
    ticket_bus_plate_number = models.CharField('Bus Plate Number', max_length=255, blank=False, default='')
    ticket_destination_name = models.CharField('Destination', max_length=255, blank=False, default='')
    ticket_schedule_id = models.CharField('Trip Id', max_length=255, blank=False, default='')
    ticket_start_bus_stop_name = models.CharField('Start Stop', max_length=255, blank=False, default='')
    ticket_end_bus_stop_name = models.CharField('End Stop', max_length=255, blank=False, default='')
    ticket_customer_name = models.CharField('Customer Name', max_length=255, blank=False, default='')
    ticket_customer_phone_number = models.CharField('Customer Phone', max_length=255, blank=False, default='')
    ticket_pos_serial_number = models.CharField('Pos', max_length=255, blank=False, default='')
    ticket_travel_date = models.CharField('Travel Date', max_length=255, blank=False, default='')
    ticket_travel_time = models.CharField('Travel Time', max_length=255, blank=False, default='')
    ticket_travel_datetime = models.DateTimeField('Travel Datetime', max_length=255, blank=False, default=None)
    ticket_price =  models.DecimalField('Ticeket Price', max_digits=30, decimal_places=2, default=Decimal(0.0))
    ticket_payment_type = models.CharField('Payment Type', max_length=255, blank=False, default='')
    ticket_payment_provider = models.CharField('Payment Provider', max_length=255, blank=False, default='')
    ticket_card_number = models.CharField('Card Number', max_length=255, blank=False, default='')
    ticket_card_response = models.TextField('Card Response', blank=True)
    ticket_card_transaction_id = models.CharField('Card Transaction Id', max_length=255, blank=False, default='')
    ticket_card_transaction_status = models.TextField('Card Transaction Status', blank=True)
    ticket_card_company_name = models.CharField('Card Company', max_length=255, blank=False, default='')
    ticket_card_old_balance = models.CharField('Card Old Balance', max_length=255, blank=False, default='')
    ticket_card_new_balance = models.CharField('Card New Balance', max_length=255, blank=False, default='')
    ticket_seat_no = models.IntegerField('Seat No.', blank=False, default=0)
    ticket_requested_at = models.IntegerField('Requested At', blank=False, default=0)
    ticket_confirmed_at = models.IntegerField('Confirmed At', blank=False, default=0)

    class Meta:
        db_table = "tickets_external"

    def __unicode__(self):
        return self.ticket_id
