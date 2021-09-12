from __future__ import unicode_literals

import itertools
from django.urls.base import reverse

import django_tables2 as tables
from django.utils.safestring import mark_safe

from app import settings
from app.models import Card_Logs
from app.utils import Utils


class CardLogsTable(tables.Table):
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
    card_log_id = tables.Column(
        verbose_name='Id',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_card_number = tables.Column(
        verbose_name='Card Number',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_amount = tables.Column(
        verbose_name='Amount',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_old_balance = tables.Column(
        verbose_name='Old Balance',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_new_balance = tables.Column(
        verbose_name='New Balance',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_response = tables.Column(
        verbose_name='Response',
        attrs={
            'search_filter': 'input-text',
        }
    )
    card_log_created_at = tables.Column(
        verbose_name='Created At',
        attrs={
            'search_filter': 'input-date',
        }
    )
    card_log_updated_at = tables.Column(
        verbose_name='Updated At',
        attrs={
            'search_filter': 'input-date',
        }
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(CardLogsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = '<a href=' + str(record.pk) + '>' + '%d' % counter + '</a>'
        return value

    @staticmethod
    def render_card_log_id(record):
        return mark_safe(
            '<a href=' + reverse("card_logs_view",
                                 args=[record.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
            str(record.card_log_id) + '</a>')

    @staticmethod
    def render_card_log_card_number(record):
        return record.card_log_card_number

    @staticmethod
    def render_card_log_amount(record):
        return record.card_log_amount

    @staticmethod
    def render_card_log_old_balance(record):
        return record.card_log_old_balance

    @staticmethod
    def render_card_log_new_balance(record):
        return record.card_log_new_balance

    @staticmethod
    def render_card_log_response(record):
        return record.card_log_response

    @staticmethod
    def render_card_log_created_at(record):
        return Utils.get_convert_datetime(record.card_log_created_at,
                                          settings.TIME_ZONE,
                                          settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

    @staticmethod
    def render_card_log_updated_at(record):
        return Utils.get_convert_datetime(record.card_log_updated_at,
                                          settings.TIME_ZONE,
                                          settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

    class Meta:
        model = Card_Logs
        order_column_index = 1
        order_column_sort = 'desc'
        attrs = {
            'id': 'table-' + Card_Logs.NAME,
            'name': Card_Logs.NAME,
            'class': 'table table-bordered table-hover thead-dark table-responsive',
            'cellspacing': '0',
            'width': '100%',
            'default_order': [order_column_index, order_column_sort],
            'table_columns': [
                {
                    "data": "row_number",
                },
                {
                    "data": "card_log_id",
                },
                {
                    "data": "card_log_card_number",
                },
                {
                    "data": "card_log_amount",
                },
                {
                    "data": "card_log_old_balance",
                },
                {
                    "data": "card_log_new_balance",
                },
                {
                    "data": "card_log_response",
                },
                {
                    "data": "card_log_created_at",
                },
                {
                    "data": "card_log_updated_at",
                },
            ],

        }
        sequence = (
            'row_number',
            'card_log_id',
            'card_log_card_number',
            'card_log_amount',
            'card_log_old_balance',
            'card_log_new_balance',
            'card_log_response',
            'card_log_created_at',
            'card_log_updated_at',
        )
        fields = (
            'card_log_id',
            'card_log_card_number',
            'card_log_amount',
            'card_log_old_balance',
            'card_log_new_balance',
            'card_log_response',
            'card_log_created_at',
            'card_log_updated_at',
        )
        template_name = '_include/bootstrap-datatable-server.html'
