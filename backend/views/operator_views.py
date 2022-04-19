import json

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
                        request, model.operator_username, model.operator_name, action_url)
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
                elif check_password(form.cleaned_data['password'], model.operator_password_hash):
                    Methods_Operators.update_status(
                        request, operator, model, Operators.STATUS_ACTIVE)
                    Operators.login(request, model)
                    Failed_Login.objects.filter(failed_login_from=Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                                failed_login_ip_address=Utils.get_ip_address(
                                                    request),
                                                failed_login_status=False).update(failed_login_status=True)
                    redirect_field_name = Operators.get_redirect_field_name(
                        request)
                    if redirect_field_name is None:
                        return redirect(reverse("operators_dashboard"))
                    else:
                        return redirect(redirect_field_name)
                else:
                    Methods_Failed_Login.add(form.cleaned_data['email'], form.cleaned_data['password'],
                                             Failed_Login.FAILED_LOGIN_FROM_BACKEND,
                                             Utils.get_ip_address(request), False)
                    messages.error(
                        request, 'Incorrect email address or password.')
                    return render(request, template_url, {'form': form, 'display_captcha': display_captcha})
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
            model.operator_password_hash = make_password(
                form.cleaned_data['new_password'])
            model.operator_password_reset_token = ''
            model.save()
            Methods_Emails.send_info_email(
                request, model.operator_username, model.operator_name, 'Your password has been updated successfully.')
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
