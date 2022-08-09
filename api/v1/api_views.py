import json
import bcrypt

from app import settings
from app.jwt import Jwt
from app.models.card_logs import Card_Logs
from app.models.methods.v2_asis import V2_Methods_Asis
from app.models.operator_access_permissions import Operator_Access_Permissions
from app.models.operators import Operators
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

from app.models.tickets_external import Tickets_External
from app.utils import Utils


def send_response(response, status):
    return Response(response, status=HTTP_200_OK, content_type="application/json")


@api_view(["POST"])
@permission_classes((AllowAny,))
@ensure_csrf_cookie
def operator_login(request):
    try:
        request_body = request.data
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
        
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(model.operator_password, 'utf-8')):
            name = str(model.operator_first_name) +' '+str(model.operator_last_name)
            access_token, expires_at = Jwt.generate_access_token(model.operator_id, { 'name': name })
            refresh_token = Jwt.generate_refresh_token(model.operator_id, { 'name': name })
            response = {
                "error": False,
                "message": 'Success',
                "data": {
                    'id': model.operator_id,
                    'username': model.operator_username,
                    'name': name,
                    'expires_at': expires_at,
                    'access_token': access_token,
                }
            }
            res = Response(response, status=HTTP_200_OK, content_type="application/json")
            res.set_cookie(key='access_token', value=access_token, httponly=True)
            res.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            return res
        
        response = {
                "error": True,
                "message": 'Incorrect username or password.',
            }
        return send_response(response, HTTP_403_FORBIDDEN)
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

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
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

        request_body = request.data
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

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
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

        request_body = request.data
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

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
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

        request_body = request.data
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

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
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

        request_body = request.data
        print(request_body)
        print(request.POST)

        amount = request_body["amount"]
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
def card_pay(request):
    try:
        payload = Jwt.authenticate(request)
        print(payload)
        if payload is None:
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)
        operator = None
        try:
            operator = Operators.objects.get(operator_id=payload['id'])
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'tickets-create' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to tickets-create. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        request_body = request.data
        print(request_body)
        print(request.POST)

        ticket = Tickets_External()
        ticket.ticket_external = 'centrika'
        ticket.ticket_reference = request_body["ticket_id"]
        ticket.ticket_company_name = request_body["company"]
        ticket.ticket_company_branch_name = request_body["branch"]
        ticket.ticket_agent_name = request_body["agent"]
        ticket.ticket_route_name = request_body["bus_route"]
        ticket.ticket_bus_plate_number = request_body["bus_plate_number"]
        ticket.ticket_schedule_id = request_body["trip_id"]
        ticket.ticket_start_bus_stop_name = request_body["start_stop"]
        ticket.ticket_end_bus_stop_name = request_body["end_stop"]
        ticket.ticket_destination_name = str(ticket.ticket_start_bus_stop_name)+'-'+str(ticket.ticket_end_bus_stop_name)
        ticket.ticket_customer_name = request_body["customer_name"]
        ticket.ticket_customer_phone_number = request_body["customer_phone"]
        ticket.ticket_pos_serial_number = request_body["pos"]
        ticket.ticket_travel_date = request_body["travel_date"]
        ticket.ticket_travel_time = request_body["travel_time"]
        ticket.ticket_travel_datetime = str(ticket.ticket_travel_date) +' '+str(ticket.ticket_travel_time)
        ticket.ticket_price = request_body["amount"]
        ticket.ticket_payment_type = 'card'
        ticket.ticket_payment_provider = 'none'
        ticket.ticket_card_number = request_body["card_number"]
        ticket.ticket_card_response = ''
        ticket.ticket_card_transaction_id = ''
        ticket.ticket_card_transaction_status = ''
        ticket.ticket_card_company_name = 'acgroup'
        ticket.ticket_card_old_balance = 0
        ticket.ticket_card_new_balance = 0
        ticket.ticket_seat_no = request_body["seat_no"]
        ticket.ticket_requested_at = Utils.get_current_datetime_utc()
        ticket.ticket_confirmed_at = 0
        ticket.save()

        error, message, access_token, session_data, card_log_id = V2_Methods_Asis.get_payment_session(
            request, operator, None, ticket.ticket_card_number, ticket.ticket_price)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)
        
        ticket.ticket_card_transaction_id = card_log_id
        ticket.save()
        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'transaction_id': ticket.ticket_id,
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
def card_pay_complete(request):
    try:
        payload = Jwt.authenticate(request)
        print(payload)
        if payload is None:
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)
        operator = None
        try:
            operator = Operators.objects.get(operator_id=payload['id'])
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            response = {
                "error": True,
                "message": 'Invalid token.',
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        if operator.operator_status != Operators.STATUS_ACTIVE and operator.operator_status != Operators.STATUS_INACTIVE:
            response = {
                "error": True,
                "message": 'Your account is not active yet. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        operator_access_permissions = Operator_Access_Permissions.objects.filter(
            operator_access_permission_operator_id=operator.operator_id).all()
        items_access_permissions = []
        for item in operator_access_permissions:
            items_access_permissions.append(
                item.operator_access_permission_name)

        if 'tickets-update' not in items_access_permissions:
            response = {
                "error": True,
                "message": 'You dont have access to tickets-update. Please contact admin for support.',
            }
            return send_response(response, HTTP_403_FORBIDDEN)

        request_body = request.data
        print(request_body)
        print(request.POST)

        ticket_id = request_body["transaction_id"]
        access_token = request_body["access_token"]
        session_data = request_body["session_data"]
        card_command = request_body["card_command"]

        try:
            ticket = Tickets_External.objects.get(
                pk=ticket_id)
        except(TypeError, ValueError, OverflowError, Tickets_External.DoesNotExist):
            return True, 'Ticket not found.', None

        try:
            card_log = Card_Logs.objects.get(
                pk=ticket.ticket_card_transaction_id)
        except(TypeError, ValueError, OverflowError, Card_Logs.DoesNotExist):
            return True, 'Card log not found.', None
        
        error, message, balance = V2_Methods_Asis.get_card_balance(
            request, operator, None, ticket.ticket_card_number, 1, card_command, access_token, session_data, card_log)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)
        
        if balance < ticket.ticket_price:
            response = {
                "error": True,
                "message": "Insufficient balance in card.",
            }
            return send_response(response, HTTP_400_BAD_REQUEST)

        error, message, card_content, card_log = V2_Methods_Asis.process_payment(
            request, operator, None, ticket.ticket_card_number, ticket.ticket_price, card_command, access_token, session_data, card_log)
        if error:
            response = {
                "error": True,
                "message": message,
            }
            return send_response(response, HTTP_400_BAD_REQUEST)
        
        ticket.ticket_card_response = card_content
        ticket.ticket_card_transaction_status = card_log.card_log_response
        ticket.ticket_card_old_balance = card_log.card_log_old_balance
        ticket.ticket_card_new_balance = card_log.card_log_new_balance
        ticket.ticket_confirmed_at = Utils.get_current_datetime_utc()
        ticket.save()

        response = {
            "error": False,
            "message": 'Success',
            "data": {
                'transaction_id': ticket.ticket_id,
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
