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
from app.models.methods.tickets_external import Methods_Tickets_External
from app.models.operators import Operators
from app.models.methods.operators import Methods_Operators
from app.models.tickets_external import Tickets_External
from app.utils import Utils
from backend.tables.tickets_external_tables import TicketsExternalTable


class AjaxTicketsExternalList(View):
    def get(self, request):
        operator = Operators.login_required(request)
        if operator is None:
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type='application/json')
        items = self._datatables(request, operator)
        return HttpResponse(json.dumps(items, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request, operator):
        auth_permissions = Methods_Operators.get_auth_permissions(operator)

        column1 = 'ticket_id'
        column2 = 'ticket_external'
        column3 = 'ticket_reference'
        column4 = 'ticket_schedule_id'
        column5 = 'ticket_travel_date'
        column6 = 'ticket_travel_time'
        column7 = 'ticket_destination_name'
        column8 = 'ticket_price'
        column9 = 'ticket_card_number'
        column10 = 'ticket_card_old_balance'
        column11 = 'ticket_card_new_balance'
        column12 = 'ticket_card_transaction_id'
        column13 = 'ticket_card_transaction_status'
        column14 = 'ticket_requested_at'
        column15 = 'ticket_confirmed_at'

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
        objects = Tickets_External.objects

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
            
            if int(order_column_index) == 9:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column9)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column9)

            if int(order_column_index) == 10:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column10)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column10)

            if int(order_column_index) == 11:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column11)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column11)

            if int(order_column_index) == 12:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column12)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column12)

            if int(order_column_index) == 13:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column13)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column13)

            if int(order_column_index) == 14:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column14)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column14)
            
            if int(order_column_index) == 15:
                if order_column_sort == 'asc':
                    objects = objects.order_by(column15)
                if order_column_sort == 'desc':
                    objects = objects.order_by('-' + column15)

        objects_filter = False
        if search:
            objects_filter = True
            objects = objects.filter(
                Q(ticket_id__icontains=search) |
                Q(ticket_external__icontains=search) |
                Q(ticket_reference__icontains=search) |
                Q(ticket_schedule_id__icontains=search) |
                Q(ticket_travel_date__icontains=search) |
                Q(ticket_travel_time__icontains=search) |
                Q(ticket_destination_name__icontains=search) |
                Q(ticket_price__icontains=search) |
                Q(ticket_card_number__icontains=search) |
                Q(ticket_card_old_balance__icontains=search) |
                Q(ticket_card_new_balance__icontains=search) |
                Q(ticket_card_transaction_id__icontains=search) |
                Q(ticket_card_transaction_status__icontains=search)
            )

        column_index = 1
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_id=column_search)
            )

        column_index = 2
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_external=column_search)
            )

        column_index = 3
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_reference=column_search)
            )

        column_index = 4
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_schedule_id=column_search)
            )

        column_index = 5
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_travel_date=column_search)
            )

        column_index = 6
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_travel_time=column_search)
            )

        column_index = 7
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_destination_name__icontains=column_search)
            )
        
        column_index = 8
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_price=column_search)
            )
        
        column_index = 9
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_card_number=column_search)
            )

        column_index = 10
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_card_old_balance=column_search)
            )
        
        column_index = 11
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_card_new_balance=column_search)
            )

        column_index = 12
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_card_transaction_id=column_search)
            )

        column_index = 13
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(ticket_card_transaction_status__icontains=column_search)
            )

        column_index = 14
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            seconds = (Utils.convert_string_to_datetime(Utils.get_format_input_date(
                column_search)+' 00:00:00')).timestamp() + settings.TIME_DIFFERENCE
            objects_filter = True
            objects = objects.filter(
                Q(ticket_requested_at__gte=seconds) &
                Q(ticket_requested_at__lt=(seconds+86400))
            )

        column_index = 15
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            seconds = (Utils.convert_string_to_datetime(Utils.get_format_input_date(
                column_search)+' 00:00:00')).timestamp() + settings.TIME_DIFFERENCE
            objects_filter = True
            objects = objects.filter(
                Q(ticket_confirmed_at__gte=seconds) &
                Q(ticket_confirmed_at__lt=(seconds+86400))
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
            data.append({
                'row_number': TicketsExternalTable.render_row_number(record, counter),
                'ticket_id': TicketsExternalTable.render_ticket_id(record),
                'ticket_external': TicketsExternalTable.render_ticket_external(record),
                'ticket_reference':  TicketsExternalTable.render_ticket_reference(record),
                'ticket_schedule_id': TicketsExternalTable.render_ticket_schedule_id(record),
                'ticket_travel_date':  TicketsExternalTable.render_ticket_travel_date(record),
                'ticket_travel_time':  TicketsExternalTable.render_ticket_travel_time(record),
                'ticket_destination_name':  TicketsExternalTable.render_ticket_destination_name(record),
                'ticket_price':  TicketsExternalTable.render_ticket_price(record),
                'ticket_card_number': TicketsExternalTable.render_ticket_card_number(record),
                'ticket_card_old_balance': TicketsExternalTable.render_ticket_card_old_balance(record),
                'ticket_card_new_balance':  TicketsExternalTable.render_ticket_card_new_balance(record),
                'ticket_card_transaction_id':  TicketsExternalTable.render_ticket_card_transaction_id(record),
                'ticket_card_transaction_status':  TicketsExternalTable.render_ticket_card_transaction_status(record),
                'ticket_requested_at':  TicketsExternalTable.render_ticket_requested_at(record),
                'ticket_confirmed_at':  TicketsExternalTable.render_ticket_confirmed_at(record),
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


def index(request):
    template_url = 'tickets-external/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_TICKETS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    
    objects = {}
    table = TicketsExternalTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_TICKETS,
            'title': Tickets_External.TITLE,
            'name': Tickets_External.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'table': table,
            'index_url': reverse("tickets_external_index"),
        }
    )


def view(request, pk):
    template_url = 'tickets-external/view.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_TICKETS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Tickets_External.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Tickets_External.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    model = Methods_Tickets_External.format_view(request, operator, model)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_TICKETS,
            'title': Tickets_External.TITLE,
            'name': Tickets_External.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'model': model,
            'index_url': reverse("tickets_external_index"),
        }
    )
