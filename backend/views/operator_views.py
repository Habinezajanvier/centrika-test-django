import json
import bcrypt

from app import settings
from app.data import ARRAY_KIGALI_AREAS, ARRAY_RWANDA_DISTRICTS
from app.models.access_permissions import Access_Permissions
from app.models.failed_login import Failed_Login
from app.models.methods.access_permissions import Methods_Access_Permissions
from app.models.methods.emails import Methods_Emails
from app.models.methods.failed_login import Methods_Failed_Login
from app.models.methods.operator_access_permissions import \
    Methods_Operator_Access_Permissions
from app.models.methods.operators import Methods_Operators
from app.models.operator_access_permissions import Operator_Access_Permissions
from app.models.operators import Operators
from app.models.organizations import Organizations
from app.utils import Utils
from backend.forms.operator_forms import (OperatorChangePasswordForm,
                                          OperatorCreateForm,
                                          OperatorForgotPasswordForm,
                                          OperatorProfileUpdateForm,
                                          OperatorResetPasswordForm,
                                          OperatorSearchIndexForm,
                                          OperatorSignInCaptchaForm,
                                          OperatorSignInForm,
                                          OperatorUpdateForm, OperatorViewForm)
from backend.tables.operator_tables import OperatorsTable
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


def confirm(request, token):
    try:
        operator = Operators.objects.get(operator_auth_key=token)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        operator = None
    if operator is None:
        messages.info(request, 'Invalid token.')
        return redirect(reverse("operators_signin"))
    model = operator
    Methods_Operators.update_status(
        request, operator, model, Operators.STATUS_UNAPPROVED)
    messages.info(
        request, 'Thank you for your email confirmation. Now you can login to your account.')
    return redirect(reverse("operators_signin"))


def signin(request):
    template_url = 'operators/signin.html'
    failed_count = Failed_Login.objects.filter(failed_login_from=Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                               failed_login_ip_address=Utils.get_ip_address(
                                                   request),
                                               failed_login_status=False).count()
    display_captcha = False
    if failed_count >= settings.MAX_LOGIN_ATTEMPTS_CAPTCHA:
        display_captcha = True
    if request.method == 'POST':
        if display_captcha:
            form = OperatorSignInCaptchaForm(request.POST)
        else:
            form = OperatorSignInForm(request.POST)
        if form.is_valid():
            try:
                operator = Operators.objects.get(
                    operator_username=form.cleaned_data['email'])
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                operator = None
            if operator is None:
                Methods_Failed_Login.add(form.cleaned_data['email'], form.cleaned_data['password'],
                                         Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                         Utils.get_ip_address(request), False)
                messages.error(
                    request, 'Incorrect email address or password3.')
                return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
            else:
                model = operator
                if model.operator_status == Operators.STATUS_UNVERIFIED:
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='operators/signup/confirm/' + model.operator_auth_key
                    )
                    Methods_Emails.send_verification_email(
                        request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), action_url)
                    messages.error(
                        request, 'Your email address is not yet verified. Please check your mail to confirm.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                elif model.operator_status == Operators.STATUS_UNAPPROVED:
                    messages.error(
                        request, 'Your account is not yet approved. Please contact admin for support.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                elif model.operator_status == Operators.STATUS_BLOCKED:
                    messages.error(
                        request, 'Your account is blocked. Please contact admin for support.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                else:
                    if not bcrypt.checkpw(bytes(form.cleaned_data['password'], 'utf-8'), bytes(model.operator_password, 'utf-8')):
                        Methods_Failed_Login.add(form.cleaned_data['email'], form.cleaned_data['password'],
                                         Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                         Utils.get_ip_address(request), False)
                        messages.error(
                            request, 'Incorrect email address or password.')
                        return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
                    
                    Methods_Operators.update_status(request, operator, model, Operators.STATUS_ACTIVE)
                    Operators.login(request, model)
                    Failed_Login.objects.filter(failed_login_from=Failed_Login.FAILED_LOGIN_FROM_BACKEND, failed_login_ip_address=Utils.get_ip_address(request),failed_login_status=False).update(failed_login_status=True)
                    redirect_field_name = Operators.get_redirect_field_name(request)
                    if redirect_field_name is None:
                        return redirect(reverse("operators_dashboard"))
                    else:
                        return redirect(redirect_field_name)
        else:
            messages.error(request, form.errors.as_data())
            return render(request, template_url, {'form': form, 'display_captcha': display_captcha})

    if display_captcha:
        form = OperatorSignInCaptchaForm()
    else:
        form = OperatorSignInForm()
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})


def forgot_password(request):
    template_url = 'operators/forgot-password.html'
    if request.method == 'POST':
        form = OperatorForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                operator = Operators.objects.get(
                    operator_username=form.cleaned_data['email'])
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                operator = None
            if operator is None:
                messages.error(
                    request, 'Email Id: "%s" is not yet registered.' % form.cleaned_data['email'])
                return render(request, template_url,
                              {'form': form})
            else:
                model = operator
                if model.operator_status == Operators.STATUS_UNVERIFIED:
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='operators/signup/confirm/' + model.operator_auth_key
                    )
                    Methods_Emails.send_verification_email(
                        request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), action_url)
                    messages.error(request,
                                   'Your email address is not yet verified. Please check your mail to confirm.')
                    return render(request, template_url,
                                  {'form': form})
                elif model.operator_status == Operators.STATUS_UNAPPROVED:
                    messages.error(
                        request, 'Your email address is not yet approved. Please contact admin for support.')
                    return render(request, template_url,
                                  {'form': form})
                elif model.operator_status == Operators.STATUS_BLOCKED:
                    messages.error(
                        request, 'Your account is blocked. Please contact admin for support.')
                    return render(request, template_url,
                                  {'form': form})
                else:
                    model.operator_password_reset_token = Operators.generate_unique_token(Operators,
                                                                                          'operator_password_reset_token')
                    model.save()
                    action_url = '{domain}/{path}'.format(
                        domain=Utils.get_backend_domain(),
                        path='operators/reset-password/' + model.operator_password_reset_token
                    )
                    Methods_Emails.send_reset_password_email(
                        request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), action_url)
                    messages.info(
                        request, 'An email has been sent to reset your password.')
                    return redirect(reverse("operators_signin"))
        else:
            form = OperatorForgotPasswordForm()
            return render(request, template_url, {'form': form})
    form = OperatorForgotPasswordForm()
    return render(request, template_url, {'form': form})


def reset_password(request, token):
    template_url = 'operators/reset-password.html'
    try:
        operator = Operators.objects.get(operator_password_reset_token=token)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        operator = None
    if operator is None:
        messages.info(request, 'Invalid token.')
        return redirect(reverse("operators_signin"))
    model = operator

    if request.method == 'POST':
        form = OperatorResetPasswordForm(request.POST)
        form.fields["email"].initial = model.operator_username
        if form.is_valid():
            # model.operator_password = make_password(form.cleaned_data['password'])
            password = bytes(form.cleaned_data['password'], 'utf-8')
            salt = bcrypt.gensalt(rounds=13)
            hashed = bcrypt.hashpw(password, salt)
            model.operator_passwordh = hashed.decode('utf-8')
            model.operator_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), 'Your password has been reset successfully.')
            messages.info(
                request, 'Your password has been reset successfully.')
            return redirect(reverse("operators_signin"))
        else:
            form.fields["email"].initial = model.operator_username
            return render(request, template_url, {'form': form})

    form = OperatorResetPasswordForm()
    form.fields["email"].initial = model.operator_username
    return render(request, template_url, {'form': form})


def signout(request):
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    model = operator
    Methods_Operators.update_status(
        request, operator, model, Operators.STATUS_INACTIVE)
    # logout
    Operators.logout(request)
    return redirect(reverse("operators_signin"))


def dashboard(request):
    template_url = 'operators/dashboard.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)

    midnight = Utils.get_midnight_datetime_utc()

    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_DASHBOARD,
            'title': 'Dashboard',
            'name': 'dashboard',
            'operator': operator,
            'auth_permissions': auth_permissions,
        }
    )


class AjaxOperatorsList(View):
    def get(self, request):
        operator = Operators.login_required(request)
        if operator is None:
            return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type='application/json')
        items = self._datatables(request, operator)
        return HttpResponse(json.dumps(items, cls=DjangoJSONEncoder), content_type='application/json')

    def _datatables(self, request, operator):
        auth_permissions = Methods_Operators.get_auth_permissions(operator)

        column1 = 'operator_username'
        column2 = 'operator_first_name'
        column3 = 'operator_phone_number'
        column4 = 'operator_organization'
        column5 = 'operator_status'

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
        objects = Operators.objects

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

        objects_filter = False
        if search:
            objects_filter = True
            organizations = Organizations.objects.filter(
                Q(organization_name__icontains=search)
            ).all()
            objects = objects.filter(
                Q(operator_username__icontains=search) |
                Q(operator_first_name__icontains=search) |
                Q(operator_last_name__icontains=search) |
                Q(operator_phone_number__icontains=search) |
                Q(operator_organization_id__in=organizations)
            )

        column_index = 1
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(operator_username__icontains=column_search)
            )

        column_index = 2
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(operator_first_name__icontains=column_search) |
                Q(operator_last_name__icontains=column_search)
            )

        column_index = 3
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(operator_phone_number__icontains=column_search)
            )

        column_index = 4
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            organizations = Organizations.objects.filter(
                Q(organization_name__icontains=column_search)
            ).all()
            objects = objects.filter(
                Q(operator_organization_id__in=organizations)
            )

        column_index = 5
        column_search = datatables.get(
            'columns[' + str(column_index) + '][search][value]')
        if column_search != '':
            objects_filter = True
            objects = objects.filter(
                Q(operator_status=Operators.ARRAY_TEXT_STATUS.index(column_search))
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
            row_number = OperatorsTable.render_row_number(record, counter)
            value1 = OperatorsTable.render_operator_username(record)
            value2 = OperatorsTable.render_operator_first_name(record)
            value3 = OperatorsTable.render_operator_phone_number(
                record)
            value4 = OperatorsTable.render_operator_organization_id(
                record, auth_permissions)
            value5 = OperatorsTable.render_operator_status(record)
            actions = OperatorsTable.render_actions(record, auth_permissions)

            data.append({
                'row_number': row_number,
                'operator_username': value1,
                'operator_first_name': value2,
                'operator_phone_number': value3,
                'operator_organization': value4,
                'operator_status': value5,
                'actions': actions,
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


def json_operators(request):
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    return HttpResponse(serializers.serialize("json", Operators.objects.all()),
                        content_type="application/json")


def index(request):
    template_url = 'operators/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    search_form = OperatorSearchIndexForm(request.POST or None)
    if request.method == 'POST' and search_form.is_valid():
        display_search = True
    else:
        display_search = False

    objects = {}
    table = OperatorsTable({})
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    table.set_auth_permissions(auth_permissions)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_OPERATORS,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'table': table,
            'search_form': search_form,
            'display_search': display_search,
            'index_url': reverse("operators_index"),
            'select_multiple_url': reverse("operators_select_multiple"),
        }
    )


@csrf_exempt
def select_single(request):
    operator = Operators.login_required(request)
    if operator is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    id = request.POST['id']
    if action == '' or id is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')
    try:
        model = Operators.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'verify':
        if model.operator_status == Operators.STATUS_UNVERIFIED:
            Methods_Operators.update_status(
                request, operator, model, Operators.STATUS_UNAPPROVED)
            messages.success(request, 'Verified successfully.')

    if action == 'approve':
        if model.operator_status == Operators.STATUS_UNAPPROVED:
            Methods_Operators.update_status(
                request, operator, model, Operators.STATUS_INACTIVE)
            messages.success(
                request, 'Approved successfully.')

    if action == 'block':
        if model.operator_status == Operators.STATUS_ACTIVE or model.operator_status == Operators.STATUS_INACTIVE:
            Methods_Operators.update_status(
                request, operator, model, Operators.STATUS_BLOCKED)
            messages.success(
                request, 'Blocked successfully.')

    if action == 'unblock':
        if model.operator_status == Operators.STATUS_BLOCKED:
            Methods_Operators.update_status(
                request, operator, model, Operators.STATUS_INACTIVE)
            messages.success(
                request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_OPERATOR_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        Methods_Operators.delete(request, model, operator)
        messages.success(request, 'Deleted successfully.')

    return HttpResponse('success', content_type='text/plain')


@csrf_exempt
def select_multiple(request):
    operator = Operators.login_required(request)
    if operator is None:
        return HttpResponse('signin', content_type='text/plain')
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    action = request.POST['action']
    ids = request.POST['ids']
    try:
        ids = ids.split(",")
    except(TypeError, ValueError, OverflowError):
        ids = None
    if action == '' or ids is None:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    if action == 'verify':
        for id in ids:
            try:
                model = Operators.objects.get(pk=id)
                if model.operator_status == Operators.STATUS_UNVERIFIED:
                    Methods_Operators.update_status(
                        request, operator, model, Operators.STATUS_UNAPPROVED)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                continue
        messages.success(request, 'Verified successfully.')

    if action == 'approve':
        for id in ids:
            try:
                model = Operators.objects.get(pk=id)
                if model.operator_status == Operators.STATUS_UNAPPROVED:
                    Methods_Operators.update_status(
                        request, operator, model, Operators.STATUS_INACTIVE)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                continue
        messages.success(request, 'Approved successfully.')

    if action == 'block':
        for id in ids:
            try:
                model = Operators.objects.get(pk=id)
                if model.operator_status == Operators.STATUS_ACTIVE or model.operator_status == Operators.STATUS_INACTIVE:
                    Methods_Operators.update_status(
                        request, operator, model, Operators.STATUS_BLOCKED)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                continue
        messages.success(request, 'Blocked successfully.')

    if action == 'unblock':
        for id in ids:
            try:
                model = Operators.objects.get(pk=id)
                if model.operator_status == Operators.STATUS_BLOCKED:
                    Methods_Operators.update_status(
                        request, operator, model, Operators.STATUS_INACTIVE)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                continue
        messages.success(request, 'Unblocked successfully.')

    if action == 'delete':
        if settings.ACCESS_PERMISSION_OPERATOR_DELETE not in auth_permissions.values():
            return HttpResponseForbidden('Forbidden', content_type='text/plain')
        for id in ids:
            try:
                model = Operators.objects.get(pk=id)
                Methods_Operators.delete(request, model, operator)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                continue
        messages.success(request, 'Deleted successfully.')

    return HttpResponse('success', content_type='text/plain')


def create(request):
    template_url = 'operators/create.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_CREATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')

    if request.method == 'POST':
        form = OperatorCreateForm(request.POST, operator=operator)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
                "name": form.cleaned_data['name'],
                "phone_number": form.cleaned_data['phone_number'],
                "organization": form.cleaned_data['organization_id'],
            }
            model = Methods_Operators.create(request, operator, data)
            action_url = '{domain}/{path}'.format(
                domain=Utils.get_backend_domain(),
                path='operators/signup/confirm/' + model.operator_auth_key
            )
            Methods_Emails.send_verification_email(
                request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), action_url)
            messages.info(
                request, 'An email has been sent for verification to your registered email address.')
            return redirect(reverse("operators_view", args=[model.operator_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_OPERATORS,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = OperatorCreateForm(operator=operator)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_OPERATORS,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )


def update(request, pk):
    template_url = 'operators/update.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Operators.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = OperatorUpdateForm(request.POST, operator=operator)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "name": form.cleaned_data['name'],
                "phone_number": form.cleaned_data['phone_number'],
                "organization": form.cleaned_data['organization_id'],
            }
            model = Methods_Operators.update(request, operator, data, model)
            messages.success(request, 'Updated successfully.')
            return redirect(reverse("operators_view", args=[model.operator_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_OPERATORS,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )

    form = OperatorUpdateForm(
        operator=operator,
        initial=Methods_Operators.form_view(request, operator, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_OPERATORS,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
        }
    )


def update_permissions_view(request, pk):
    template_url = 'operators/update-permissions.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Operators.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = OperatorUpdateForm(request.POST, operator=operator)
        if form.is_valid():
            model.save()
            messages.success(
                request, 'Updated permissions successfully.')
            return redirect(reverse("operators_view", args=[model.operator_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_OPERATORS,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )

    form = OperatorUpdateForm(
        operator=operator,
        initial=Methods_Operators.form_view(request, operator, model)
    )
    form.fields['name'].widget.attrs['readonly'] = 'true'
    form.fields['name'].widget.attrs['disabled'] = 'true'
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_OPERATORS,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
            'all_auth_permissions': Methods_Access_Permissions.get_access_permissions(),
            'operator_auth_permissions': Methods_Operator_Access_Permissions.get_access_permissions(
                model.operator_id),
        }
    )


def update_permissions_action(request):
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    id = request.POST['id']
    permissions = request.POST['permissions']
    print(permissions)
    permissions_list = None
    if permissions != '' and permissions != 'null':
        permissions_list = permissions.split(",")
        print(len(permissions_list))
    print(permissions_list)
    try:
        model = Operators.objects.get(pk=id)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if permissions_list is not None:
        # delete existing permissions
        Operator_Access_Permissions.objects.filter(operator_access_permission_operator_id=id).delete()
        i = 0
        while i < len(permissions_list):
            if permissions_list[i]:
                access_permission = Access_Permissions.objects.get(
                    access_permission_name=permissions_list[i])
                operator_access_permission = Operator_Access_Permissions()
                operator_access_permission.operator_access_permission_name = access_permission.access_permission_name
                operator_access_permission.operator_access_permission_operator_id = id
                operator_access_permission.operator_access_permission_updated_at = Utils.get_current_datetime_utc()
                operator_access_permission.operator_access_permission_updated_by = operator.operator_id
                operator_access_permission.save()
            i += 1
    messages.success(request, 'Updated permissions successfully.')
    return HttpResponse('success', content_type='text/plain')


def update_reset_password(request, pk):
    template_url = 'operators/update-reset-password.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Operators.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    if request.method == 'POST':
        form = OperatorResetPasswordForm(request.POST)
        form.fields["email"].initial = model.operator_username
        if form.is_valid():
            # model.operator_password = make_password(form.cleaned_data['password'])
            password = bytes(form.cleaned_data['password'], 'utf-8')
            salt = bcrypt.gensalt(rounds=13)
            hashed = bcrypt.hashpw(password, salt)
            model.operator_password = hashed.decode('utf-8')
            model.operator_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), 'Your password has been reset successfully by admin.')
            messages.info(request, 'Password has been reset successfully.')
            return redirect(reverse("operators_view", args=[model.operator_id]))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                    'model': model,
                }
            )
    form = OperatorResetPasswordForm()
    form.fields["email"].initial = model.operator_username
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
            'model': model,
        }
    )


def view(request, pk):
    template_url = 'operators/view.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_VIEW not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    try:
        model = Operators.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
        return HttpResponseNotFound('Not Found', content_type='text/plain')
    model = Methods_Operators.format_view(request, operator, model)
    form = OperatorViewForm(
        operator=operator,
        initial=Methods_Operators.form_view(request, operator, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_OPERATORS,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'model': model,
            'form': form,
            'index_url': reverse("operators_index"),
            'select_single_url': reverse("operators_select_single"),
        }
    )


def profile_view(request):
    template_url = 'operators/profile-view.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    model = operator
    model = Methods_Operators.format_view(request, operator, model)
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'model': model,
        }
    )


def profile_update(request):
    template_url = 'operators/profile-update.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    model = operator
    if request.method == 'POST':
        form = OperatorProfileUpdateForm(request.POST)
        if form.is_valid():
            data = {
                "email": form.cleaned_data['email'],
                "name": form.cleaned_data['name'],
                "phone_number": form.cleaned_data['phone_number'],
            }
            model = Methods_Operators.update(request, operator, data, model)
            messages.success(request, 'Updated successfully.')
            return redirect(reverse("operators_profile_view"))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = OperatorProfileUpdateForm(
        initial=Methods_Operators.form_view(request, operator, model)
    )
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )


def profile_change_password(request):
    template_url = 'operators/profile-change-password.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    auth_permissions = Methods_Operators.get_auth_permissions(operator)
    if settings.ACCESS_PERMISSION_OPERATOR_UPDATE not in auth_permissions.values():
        return HttpResponseForbidden('Forbidden', content_type='text/plain')
    model = operator
    if request.method == 'POST':
        form = OperatorChangePasswordForm(request.POST)
        form.fields["email"].initial = model.operator_username
        if form.is_valid():
            # model.operator_password = make_password(form.cleaned_data['new_password'])
            password = bytes(form.cleaned_data['password'], 'utf-8')
            salt = bcrypt.gensalt(rounds=13)
            hashed = bcrypt.hashpw(password, salt)
            model.operator_password = hashed.decode('utf-8')
            model.operator_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.operator_username, str(model.operator_first_name) + ' '+ str(model.operator_last_name), 'Your password has been updated successfully.')
            messages.info(
                request, 'Your password has been changed successfully.')
            return redirect(reverse("operators_profile_view"))
        else:
            messages.warning(request, form.errors)
            return render(
                request, template_url,
                {
                    'section': settings.BACKEND_SECTION_PROFILE,
                    'title': Operators.TITLE,
                    'name': Operators.NAME,
                    'operator': operator,
                    'auth_permissions': auth_permissions,
                    'form': form,
                }
            )

    form = OperatorChangePasswordForm()
    form.fields["email"].initial = model.operator_username
    return render(
        request, template_url,
        {
            'section': settings.BACKEND_SECTION_PROFILE,
            'title': Operators.TITLE,
            'name': Operators.NAME,
            'operator': operator,
            'auth_permissions': auth_permissions,
            'form': form,
        }
    )