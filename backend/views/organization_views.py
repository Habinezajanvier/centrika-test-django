import json

from app import settings
from app.models.methods.operators import Methods_Operators
from app.models.methods.organizations import Methods_Organizations
from app.models.operators import Operators
from app.models.organizations import Organizations
from backend.forms.organization_forms import (OrganizationCreateForm,
                                              OrganizationSearchIndexForm,
                                              OrganizationUpdateForm,
                                              OrganizationViewForm)
from backend.tables.organization_tables import OrganizationsTable
from django.contrib import messages
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class AjaxOrganizationsList(View):
    def get(self, request):
        operator = Operators.login_required(request)
        if operator is None:
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type='application/json')
        items = self._datatables(request, operator)
        return HttpResponse(json.dumps(items, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request, operator):
        auth_permissions = Methods_Operators.get_auth_permissions(operator)

        column1 = 'organization_name'
        column2 = 'organization_email_id'
        column3 = 'organization_phone_number'
        column4 = 'organization_status'

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
        objects = Organizations.objects

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

        objects_filter = False
        if search:
            objects_filter = True
            objects = objects.filter(
                Q(organization_name__icontains=search) |
                Q(organization_email_id__icontains=search) |
                Q(organization_phone_number__icontains=search) |
                Q(organization_status=search)
            )

        column_index = 1
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(organization_name__icontains=column_search)
            )

        column_index = 2
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(organization_email_id__icontains=column_search)
            )

        column_index = 3
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(organization_phone_number__icontains=column_search)
            )

        column_index = 4
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(organization_status=Organizations.ARRAY_TEXT_STATUS.index(column_search))
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
            row_number = OrganizationsTable.render_row_number(record, counter)
            value1 = OrganizationsTable.render_organization_name(record)
            value2 = OrganizationsTable.render_organization_email_id(record)
            value3 = OrganizationsTable.render_organization_phone_number(
                record)
            value4 = OrganizationsTable.render_organization_status(record)
            actions = OrganizationsTable.render_actions(
                record, auth_permissions)

            data.append({
                'row_number': row_number,
                'organization_name': value1,
                'organization_email_id': value2,
                'organization_phone_number': value3,
                'organization_status': value4,
                'actions': actions,
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


def json_organizations(request):
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    return HttpResponse(serializers.serialize("json", Organizations.objects.all()),
                        content_type="application/json")


def index(request):
    template_url = 'organizations/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    search_form = OrganizationSearchIndexForm(request.POST or None)
    if request.method == 'POST' and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    table = OrganizationsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_ORGANIZATIONS,
            'title': Organizations.TITLE,
            'name': Organizations.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'table': table,
            'search_form': search_form,
            'display_search': display_search,
            'index_url': reverse("organizations_index"),
            'select_multiple_url': reverse("organizations_select_multiple"),
        }
    )


@csrf_exempt
def select_single(request):
    operator = Operators.login_required(request)
    if operator is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    id = request.POST['id']
    if action == '' or id is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')
    try:
        model = Organizations.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'block':
        if model.organization_status == Organizations.STATUS_ACTIVE:
            Methods_Organizations.update_status(
                request, operator, model, Organizations.STATUS_BLOCKED)
            messages.success(
                request, 'Blocked successfully.')

    if action == 'unblock':
        if model.organization_status == Organizations.STATUS_BLOCKED:
            Methods_Organizations.update_status(
                request, operator, model, Organizations.STATUS_ACTIVE)
            messages.success(
                request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        Methods_Organizations.delete(request, model, operator)
        messages.success(request, 'Deleted successfully.')

    return HttpResponse('success', content_type='text/plain')


@csrf_exempt
def select_multiple(request):
    operator = Operators.login_required(request)
    if operator is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    ids = request.POST['ids']
    try:
        ids = ids.split(",")
    except(TypeError, ValueError, OverflowError):
        ids = None
    if action == '' or ids is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'block':
        for id in ids:
            try:
                model = Organizations.objects.get(pk=id)
                if model.organization_status == Organizations.STATUS_ACTIVE or model.organization_status == Organizations.STATUS_INACTIVE:
                    Methods_Organizations.update_status(
                        request, operator, model, Organizations.STATUS_BLOCKED)
            except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, 'Blocked successfully.')

    if action == 'unblock':
        for id in ids:
            try:
                model = Organizations.objects.get(pk=id)
                if model.organization_status == Organizations.STATUS_BLOCKED:
                    Methods_Organizations.update_status(
                        request, operator, model, Organizations.STATUS_ACTIVE)
            except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_ORGANIZATIONS_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        for id in ids:
            try:
                model = Organizations.objects.get(pk=id)
                Methods_Organizations.delete(request, model, operator)
            except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
                continue
        messages.success(request, 'Deleted successfully.')

    return HttpResponse('success', content_type='text/plain')


def create(request):
    template_url = 'organizations/create.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_CREATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    if request.method == 'POST':
        form = OrganizationCreateForm(
            request.POST, operator=operator, model=None)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "phone_number": form.cleaned_data['phone_number'],
            }
            model = Methods_Organizations.create(request, operator, data)
            messages.info(
                request, 'Created successfully.')
            return redirect(reverse("organizations_view", args=[model.organization_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_ORGANIZATIONS,
                    'title': Organizations.TITLE,
                    'name': Organizations.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = OrganizationCreateForm(operator=operator, model=None)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_ORGANIZATIONS,
            'title': Organizations.TITLE,
            'name': Organizations.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )


def update(request, pk):
    template_url = 'organizations/update.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Organizations.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = OrganizationUpdateForm(
            request.POST, operator=operator, model=model)
        if form.is_valid():
            data = {
                "name": form.cleaned_data['name'],
                "email": form.cleaned_data['email'],
                "phone_number": form.cleaned_data['phone_number'],
            }
            model = Methods_Organizations.update(
                request, operator, data, model)
            messages.success(request, 'Updated successfully.')
            return redirect(reverse("organizations_view", args=[model.organization_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_ORGANIZATIONS,
                    'title': Organizations.TITLE,
                    'name': Organizations.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )

    form = OrganizationUpdateForm(
        operator=operator, model=model,
        initial=Methods_Organizations.form_view(request, operator, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_ORGANIZATIONS,
            'title': Organizations.TITLE,
            'name': Organizations.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
        }
    )


def view(request, pk):
    template_url = 'organizations/view.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_ORGANIZATIONS_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Organizations.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    model = Methods_Organizations.format_view(request, operator, model)
    form = OrganizationViewForm(
        operator=operator, model=model,
        initial=Methods_Organizations.form_view(request, operator, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_ORGANIZATIONS,
            'title': Organizations.TITLE,
            'name': Organizations.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'model': model,
            'form': form,
            'index_url': reverse("organizations_index"),
            'select_single_url': reverse("organizations_select_single"),
        }
    )