import json
import os
import string
import time

import requests
from django.contrib import messages
from django.core.files import File
from django.core.management import call_command
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from app import settings
from app.models.operators import Operators
from app.models.methods.operators import Methods_Operators
from app.utils import Utils
from backend.forms.setting_forms import SettingExcelImportForm
from backend.views.setting_views import HttpResponseForbidden


@csrf_exempt
def temp_upload(request):
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    else:
        if request.POST:
            file_path = settings.MEDIA_ROOT + '/temp/' + request.POST['name']
            image_data = request.POST['data']
            Utils.save_image_base64(image_data, file_path)
            return HttpResponse('success')
        else:
            return HttpResponseBadRequest('no data')


@csrf_exempt
def generate_qr_code(data, size=10, border=0):
    print("QR Data: " + data)
    import qrcode
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()


@csrf_exempt
def get_qr_code_image(request, size, text):
    print(size)
    print(text)
    qr = generate_qr_code(text, 10, 2)
    response = HttpResponse()
    qr.save(response, "PNG")
    return response


def index(request):
    template_url = 'settings/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    else:
        auth_permissions = Methods_Operators.get_auth_permissions(operator)
        return render(
            request, template_url,
            {
                'section': settings.BACKEND_SECTION_SETTINGS,
                'title': 'Settings',
                'name': 'settings',
                'operator': operator,
                'auth_permissions': auth_permissions,
            }
        )


def update_database(request):
    template_url = 'settings/index.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    else:
        auth_permissions = Methods_Operators.get_auth_permissions(operator)

        # messages.success(request, 'Updated successfully.')
        return redirect(reverse("settings_index"))


def excel_import(request):
    template_url = 'settings/import-excel.html'
    operator = Operators.login_required(request)
    if operator is None:
        Operators.set_redirect_field_name(request, request.path)
        return redirect(reverse("operators_signin"))
    else:
        auth_permissions = Methods_Operators.get_auth_permissions(operator)
        return HttpResponseNotFound('Not Found', content_type='text/plain')
