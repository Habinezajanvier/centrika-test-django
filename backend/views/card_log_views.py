from app.models.methods.card_logs import Methods_Card_Logs
from app.models.card_logs import Card_Logs
import base64
import json
import os

import requests
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseServerError
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from app import settings
from app.models.operators import Operators
from app.models.methods.operators import Methods_Operators
from app.utils import Utils
from backend.tables.card_log_tables import CardLogsTable


class AjaxCardLogsList(View):
    def get(self, request):
        operator = Operators.login_required(request)
        if operator is None:
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type='application/json')
        items = self._datatables(request, operator)
        return HttpResponse(json.dumps(items, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request, operator):
        auth_permissions = Methods_Operators.get_auth_permissions(operator)

        column1 = 'card_log_id'
        column2 = 'card_log_card_number'
        column3 = 'card_log_amount'
        column4 = 'card_log_old_balance'
        column5 = 'card_log_new_balance'
        column6 = 'card_log_response'
        column7 = 'card_log_created_at'
        column8 = 'card_log_updated_at'

        datatables = request.GET

        # item draw
        draw = int(datatables.get('draw'))
        # item start
        start = int(datatables.get('start'))
        # item length (limit)
        length = int(datatables.get('length'))
        # item data search
        search = datatables.get('search[value]')

        # Get objects
        objects = Card_Logs.objects

        # Set record total
        records_total = objects.all().count()
        # Set records filtered
        records_filtered = records_total

        order_column_index = datatables.get('order[0][column]')
        order_column_sort = datatables.get('order[0][dir]')

        if order_column_index and order_column_sort:
            if int(order_column_index) == 1:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column1)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column1)

            if int(order_column_index) == 2:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column2)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column2)

            if int(order_column_index) == 3:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column3)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column3)

            if int(order_column_index) == 4:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column4)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column4)

            if int(order_column_index) == 5:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column5)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column5)

            if int(order_column_index) == 6:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column6)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column6)

            if int(order_column_index) == 7:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column7)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column7)

            if int(order_column_index) == 8:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column8)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column8)

        objects_filter = False
        if search:
            objects_filter = True
            objects = objects.filter(
                Q(card_log_card_number__icontains=search) |
                Q(card_log_amount__icontains=search) |
                Q(card_log_old_balance__icontains=search) |
                Q(card_log_new_balance__icontains=search) |
                Q(card_log_response__icontains=search)
            )

        column_index = 1
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_id=column_search)
            )

        column_index = 2
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_card_number__icontains=column_search)
            )

        column_index = 3
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_amount__icontains=column_search)
            )

        column_index = 4
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_old_balance__icontains=column_search)
            )

        column_index = 5
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_new_balance__icontains=column_search)
            )

        column_index = 6
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(card_log_response__icontains=column_search)
            )

        column_index = 7
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            seconds = (Utils.convert_string_to_datetime(Utils.get_format_input_date(
                column_search)+' 00:00:00')).timestamp() + settings.TIME_DIFFERENCE
            objects_filter = True
            objects = objects.filter(
                Q(card_log_created_at__gte=seconds) &
                Q(card_log_created_at__lt=(seconds+86400))
            )

        column_index = 8
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            seconds = (Utils.convert_string_to_datetime(Utils.get_format_input_date(
                column_search)+' 00:00:00')).timestamp() + settings.TIME_DIFFERENCE
            objects_filter = True
            objects = objects.filter(
                Q(card_log_updated_at__gte=seconds) &
                Q(card_log_updated_at__lt=(seconds+86400))
            )

        if objects_filter:
            records_filtered = objects.all().count()

        items = objects.all()

        if length == -1:
            paginator = Paginator(items, items.count())
            page_number = 1
        else:
            paginator = Paginator(items, length)
            page_number = start / length + 1

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        counter = 0
        data = []
        for record in object_list:
            counter = counter + 1
            row_number = CardLogsTable.render_row_number(record, counter)
            value1 = CardLogsTable.render_card_log_id(record)
            value2 = CardLogsTable.render_card_log_card_number(
                record)
            value3 = CardLogsTable.render_card_log_amount(
                record)
            value4 = CardLogsTable.render_card_log_old_balance(
                record)
            value5 = CardLogsTable.render_card_log_new_balance(
                record)
            value6 = CardLogsTable.render_card_log_response(
                record)
            value7 = CardLogsTable.render_card_log_created_at(record)
            value8 = CardLogsTable.render_card_log_updated_at(record)

            data.append({
                'row_number': row_number,
                'card_log_id': value1,
                'card_log_card_number': value2,
                'card_log_amount': value3,
                'card_log_old_balance': value4,
                'card_log_new_balance': value5,
                'card_log_response': value6,
                'card_log_created_at': value7,
                'card_log_updated_at': value8,
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


def index(request):
    template_url = 'card-logs/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_LOG_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    
    objects = {}
    table = CardLogsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_LOGS,
            'title': Card_Logs.TITLE,
            'name': Card_Logs.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'table': table,
            'index_url': reverse("card_logs_index"),
        }
    )


def view(request, pk):
    template_url = 'card-logs/view.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_LOG_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Card_Logs.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Card_Logs.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    model = Methods_Card_Logs.format_view(request, operator, model)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_LOGS,
            'title': Card_Logs.TITLE,
            'name': Card_Logs.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'model': model,
            'index_url': reverse("card_logs_index"),
        }
    )
