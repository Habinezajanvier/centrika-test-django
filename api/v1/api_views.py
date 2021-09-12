import json

from app import settings
from app.models.card_logs import Card_Logs
from app.models.methods.v2_asis import V2_Methods_Asis
from app.models.operator_access_permissions import Operator_Access_Permissions
from app.models.operators import Operators
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)


def send_response(response, status):
    return Response(response, status=HTTP_200_OK, content_type="application/json")


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def operator_login(request):
    try:
        print(request.headers)
        api_token = request.headers['x-auth']
        if api_token != settings.API_TOKEN:
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        print(request.body)
        request_body = json.loads(request.body, encoding='utf-8')
        print(request_body)
        print(request.POST)

        username = request_body["username"]
        password = request_body["password"]

        try:
            model = Operators.objects.get(
                Q(operator_username=username)
            )
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Incorrect username or password.',
            }
            return send_response(response, HTTP_404_NOT_FOUND)

        if model.operator_status != Operators.STATUS_ACTIVE and model.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        if not check_password(password, model.operator_password_hash):
            response = {
                "error": True,
                "message": 'Incorrect username or password.',
            }
            return send_response(response, HTTP_404_NOT_FOUND)

        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'id': model.operator_id,
                'name': model.operator_name,
                'token': model.operator_auth_key,
                'username': model.operator_username,
            }
        }
        return send_response(response, HTTP_200_OK)
    except Exception as e:
        response = {
            "error": True,
            "message": 'Exception: ' + str(e),
        }
        return send_response(response, HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def card_topup(request):
    try:
        print(request.headers)
        api_token = request.headers['x-auth']
        try:
            operator = Operators.objects.get(operator_auth_key=api_token)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'card-topup' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to card-topup. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        print(request.body)
        request_body = json.loads(request.body, encoding='utf-8')
        print(request_body)
        print(request.POST)

        amount = request_body["amount"]
        card_number = request_body["card_number"]

        error, message, access_token, session_data, card_log_id = V2_Methods_Asis.get_payment_session(
            request, operator, None, card_number, amount)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)
        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'amount': amount,
                'card_number': card_number,
                'card_log_id': card_log_id,
                'access_token': access_token,
                'session_data': session_data,
            }
        }
        return send_response(response, HTTP_200_OK)
    except Exception as e:
        response = {
            "error": True,
            "message": 'Exception: ' + str(e),
        }
        return send_response(response, HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def card_topup_complete(request):
    try:
        print(request.headers)
        api_token = request.headers['x-auth']
        try:
            operator = Operators.objects.get(operator_auth_key=api_token)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'card-topup' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to card-topup. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        print(request.body)
        request_body = json.loads(request.body, encoding='utf-8')
        print(request_body)
        print(request.POST)

        amount = request_body["amount"]
        card_number = request_body["card_number"]
        card_log_id = request_body["card_log_id"]
        access_token = request_body["access_token"]
        card_command = request_body["card_command"]
        session_data = request_body["session_data"]

        try:
            card_log = Card_Logs.objects.get(
                pk=card_log_id)
        except(TypeError, ValueError, OverflowError, Card_Logs.DoesNotExist):
            return True, 'Card log not found.', None

        error, message, response_content = V2_Methods_Asis.validate_card_topup(
            request, operator, None, card_number, amount, card_command, access_token, session_data, card_log, None)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        # topup api not asis
        error, message, data = V2_Methods_Asis.card_topup(
            request, operator, card_number, amount)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        error, message, card_content = V2_Methods_Asis.process_card_topup(
            request, operator, None, card_number, amount, card_command, access_token, session_data, card_log, None)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'amount': amount,
                'card_number': card_number,
                'card_log_id': card_log_id,
                'access_token': access_token,
                'card_content': card_content,
            }
        }
        return send_response(response, HTTP_200_OK)
    except Exception as e:
        response = {
            "error": True,
            "message": 'Exception: ' + str(e),
        }
        return send_response(response, HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def card_balance(request):
    try:
        print(request.headers)
        api_token = request.headers['x-auth']
        try:
            operator = Operators.objects.get(operator_auth_key=api_token)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'card-fetch-balance' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to card-fetch-balance. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        print(request.body)
        request_body = json.loads(request.body, encoding='utf-8')
        print(request_body)
        print(request.POST)

        card_number = request_body["card_number"]

        error, message, access_token, session_data, card_log_id = V2_Methods_Asis.get_payment_session(
            request, operator, None, card_number, 0)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'card_number': card_number,
                'card_log_id': card_log_id,
                'access_token': access_token,
                'session_data': session_data,
            }
        }
        return send_response(response, HTTP_200_OK)
    except Exception as e:
        response = {
            "error": True,
            "message": 'Exception: ' + str(e),
        }
        return send_response(response, HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def card_balance_complete(request):
    try:
        print(request.headers)
        api_token = request.headers['x-auth']
        try:
            operator = Operators.objects.get(operator_auth_key=api_token)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'card-fetch-balance' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to card-fetch-balance. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        print(request.body)
        request_body = json.loads(request.body, encoding='utf-8')
        print(request_body)
        print(request.POST)

        card_number = request_body["card_number"]
        card_log_id = request_body["card_log_id"]
        access_token = request_body["access_token"]
        session_data = request_body["session_data"]
        card_command = request_body["card_command"]

        try:
            card_log = Card_Logs.objects.get(
                pk=card_log_id)
        except(TypeError, ValueError, OverflowError, Card_Logs.DoesNotExist):
            return True, 'Card log not found.', None

        error, message, balance = V2_Methods_Asis.get_card_balance(
            request, operator, None, card_number, 0, card_command, access_token, session_data, card_log, None)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'card_number': card_number,
                'card_log_id': card_log_id,
                'access_token': access_token,
                'card_balance': balance,
            }
        }
        return send_response(response, HTTP_200_OK)
    except Exception as e:
        response = {
            "error": True,
            "message": 'Exception: ' + str(e),
        }
        return send_response(response, HTTP_500_INTERNAL_SERVER_ERROR)
