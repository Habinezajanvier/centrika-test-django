from __future__ import unicode_literals

import itertools
from django.urls.base import reverse

import django_tables2 as tables
from django.utils.safestring import mark_safe

from app import settings
from app.models import Tickets_External
from app.utils import Utils


class TicketsExternalTable(tables.Table):
    auth_permissions = {}

    row_number = tables.Column(
        verbose_name='Id',
        attrs={
            'search_filter': '',
            'th_style': 'width:60px;',
        },
        orderable=False,
        empty_values=(),
        accessor='pk',
    )
    ticket_id = tables.Column(
        verbose_name='Id',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_external = tables.Column(
        verbose_name='Organization',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_reference = tables.Column(
        verbose_name='Reference',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_schedule_id = tables.Column(
        verbose_name='Trip',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_travel_date = tables.Column(
        verbose_name='TravelDate',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_destination_name = tables.Column(
        verbose_name='TravelTime',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_travel_time = tables.Column(
        verbose_name='TravelTime',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_price = tables.Column(
        verbose_name='Amount',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_card_number = tables.Column(
        verbose_name='CardNumber',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_card_old_balance = tables.Column(
        verbose_name='OldBalance',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_card_new_balance = tables.Column(
        verbose_name='NewBalance',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_card_transaction_id = tables.Column(
        verbose_name='CardLogId',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_card_transaction_status = tables.Column(
        verbose_name='TransactionStatus',
        attrs={
            'search_filter': 'input-text',
        }
    )
    ticket_requested_at = tables.Column(
        verbose_name='RequestedAt',
        attrs={
            'search_filter': 'input-date',
        }
    )
    ticket_confirmed_at = tables.Column(
        verbose_name='ConfirmedAt',
        attrs={
            'search_filter': 'input-date',
        }
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(TicketsExternalTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = '<a href=' + str(record.pk) + '>' + '%d' % counter + '</a>'
        return value

    @staticmethod
    def render_ticket_id(record):
        return mark_safe(
            '<a href=' + reverse("tickets_external_view",
                                 args=[record.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
            str(record.ticket_id) + '</a>')

    @staticmethod
    def render_ticket_external(record):
        return record.ticket_external
    
    @staticmethod
    def render_ticket_reference(record):
        return record.ticket_reference
    
    @staticmethod
    def render_ticket_schedule_id(record):
        return record.ticket_schedule_id
    
    @staticmethod
    def render_ticket_travel_date(record):
        return record.ticket_travel_date
    
    @staticmethod
    def render_ticket_travel_time(record):
        return record.ticket_travel_time
    
    @staticmethod
    def render_ticket_destination_name(record):
        return record.ticket_destination_name
    
    @staticmethod
    def render_ticket_price(record):
        return record.ticket_price
    
    @staticmethod
    def render_ticket_card_number(record):
        return record.ticket_card_number
    
    @staticmethod
    def render_ticket_card_old_balance(record):
        return record.ticket_card_old_balance
    
    @staticmethod
    def render_ticket_card_new_balance(record):
        return record.ticket_card_new_balance
    
    @staticmethod
    def render_ticket_card_transaction_id(record):
        return record.ticket_card_transaction_id
    
    @staticmethod
    def render_ticket_card_transaction_status(record):
        return record.ticket_card_transaction_status

    @staticmethod
    def render_ticket_requested_at(record):
        return Utils.get_convert_datetime(record.ticket_requested_at,
                                          settings.TIME_ZONE,
                                          settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

    @staticmethod
    def render_ticket_confirmed_at(record):
        return Utils.get_convert_datetime(record.ticket_confirmed_at,
                                          settings.TIME_ZONE,
                                          settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

    class Meta:
        model = Tickets_External
        order_column_index = 1
        order_column_sort = 'desc'
        attrs = {
            'id': 'table-' + Tickets_External.NAME,
            'name': Tickets_External.NAME,
            'class': 'table table-bordered table-hover thead-dark table-responsive',
            'cellspacing': '0',
            'width': '100%',
            'default_order': [order_column_index, order_column_sort],
            'table_columns': [
                {
                    "data": "row_number",
                },
                {
                    "data": "ticket_id",
                },
                {
                    "data": "ticket_external",
                },
                {
                    "data": "ticket_reference",
                },
                {
                    "data": "ticket_schedule_id",
                },
                {
                    "data": "ticket_travel_date",
                },
                {
                    "data": "ticket_travel_time",
                },
                {
                    "data": "ticket_destination_name",
                },
                {
                    "data": "ticket_price",
                },
                {
                    "data": "ticket_card_number",
                },
                {
                    "data": "ticket_card_old_balance",
                },
                {
                    "data": "ticket_card_new_balance",
                },
                {
                    "data": "ticket_card_transaction_id",
                },
                {
                    "data": "ticket_card_transaction_status",
                },
                {
                    "data": "ticket_requested_at",
                },
                {
                    "data": "ticket_confirmed_at",
                },
            ],

        }
        sequence = (
            'row_number',
            'ticket_id',
            'ticket_external',
            'ticket_reference',
            'ticket_schedule_id',
            'ticket_travel_date',
            'ticket_travel_time',
            'ticket_destination_name',
            'ticket_price',
            'ticket_card_number',
            'ticket_card_old_balance',
            'ticket_card_new_balance',
            'ticket_card_transaction_id',
            'ticket_card_transaction_status',
            'ticket_requested_at',
            'ticket_confirmed_at',
        )
        fields = (
            'ticket_id',
            'ticket_external',
            'ticket_reference',
            'ticket_schedule_id',
            'ticket_travel_date',
            'ticket_travel_time',
            'ticket_destination_name',
            'ticket_price',
            'ticket_card_number',
            'ticket_card_old_balance',
            'ticket_card_new_balance',
            'ticket_card_transaction_id',
            'ticket_card_transaction_status',
            'ticket_requested_at',
            'ticket_confirmed_at',
        )
        template_name = '_include/bootstrap-datatable-server.html'
