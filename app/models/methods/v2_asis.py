from app.models.card_logs import Card_Logs
from app import settings
from app.utils import Utils
from datetime import datetime, time
import json
import uuid
import requests

from app import models
from django.db import models


class V2_Methods_Asis():
    ASIS_URL = 'http://asis-services.com/RuandaPaymentApiV2/api/'
    ASIS_TOP_UP_API_TOKEN = 'cp/}6dr;<#r2;9ZU6V}S/:"*H%h*4_@g'

    # Test Cards
    ASIS_TEST_CARD_1 = '006457cf'

    # Login
    ASIS_TOKEN_URL = ASIS_URL + 'Token/Post'
    ASIS_USERNAME = 'Rwapi21v2'  #'Ruanda.api', ''
    ASIS_PASSWORD = '*23Iisaisbu'  #'As123456', ''
    ASIS_GRANT_TYPE = ''
    # Session
    ASIS_SESSION_URL = ASIS_URL + 'Purse/StartSession'
    ASIS_END_SESSION_URL = ASIS_URL + 'Purse/EndSession/'
    ASIS_NETWORK_ID = 180
    ASIS_INSTITUTION_CODE = 'INTERCITY'  # Tap&GO Ride, INTERCITY, Shuttles
    ASIS_DEVICE_SERIAL_NUMBER = '14001'  # 10003, 14001, 13901
    # Get/Pay
    ASIS_GETPURSE_URL = ASIS_URL + 'Purse/GetPurse/'
    ASIS_PAYPURSE_URL = ASIS_URL + 'Purse/WebTopUp/'

    # call apis
    @classmethod
    def ap_login_token(cls, request, card_log):
        try:
            url = V2_Methods_Asis.ASIS_TOKEN_URL
            payload = 'grant_type=password&userName='+V2_Methods_Asis.ASIS_USERNAME+'&password='+V2_Methods_Asis.ASIS_PASSWORD
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 11: API called failed from ASIS. Response: '+str(response), None

            # update card log
            card_log.card_log_login_request_body = payload
            card_log.card_log_login_response = result
            card_log.card_log_updated_at = Utils.get_current_datetime_utc()
            card_log.save()

            data = json.loads(result)
            access_token = data['access_token']
            return False, 'Success', access_token
        except Exception as e:
            return True, 'Error 1: API called failed from ASIS. Response: '+str(e), None

    @classmethod
    def api_start_session(cls, request, operator, device, card_log, access_token, client_session_id, card_number):
        try:
            time_in_formatted = Utils.get_convert_datetime_other(
                Utils.get_current_datetime_utc(), settings.TIME_ZONE, settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' GMT+02:00'
            url = V2_Methods_Asis.ASIS_SESSION_URL
            payload = {
                'header': {
                    'versionSchema': 1,
                    'clientSessionId': client_session_id,
                    # V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER, device.device_asis_serial_no
                    'deviceSerialNo': V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER,
                    'dateTime': time_in_formatted,
                    'networkId': V2_Methods_Asis.ASIS_NETWORK_ID,
                    'institutionCode': V2_Methods_Asis.ASIS_INSTITUTION_CODE,
                },
                'content': {
                    'media': {
                        'type': 'MfrV2',
                        'mediaUniqueId': card_number,
                        'atq': '0400',
                        'sak': 8,
                    }
                },
            }
            payload = json.dumps(payload)
            payload = str(payload)
            headers = {
                'Authorization': 'Bearer '+str(access_token),
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 21: API called failed from ASIS. Response: '+str(response), None

            # update card log
            card_log.card_log_start_session_request_body = payload
            card_log.card_log_start_session_response = result
            card_log.card_log_updated_at = Utils.get_current_datetime_utc()
            card_log.save()

            data = json.loads(result)
            message = data['result']['message']
            if message is not None:
                return True, 'Error 22: API called failed from ASIS. Response: '+str(message), None
            return False, 'Success', data
        except Exception as e:
            return True, 'Error 2: API called failed from ASIS. Response: '+str(e), None

    @classmethod
    def api_pay_purse(cls, request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command):
        try:
            time_in_formatted = Utils.get_convert_datetime_other(
                Utils.get_current_datetime_utc(), settings.TIME_ZONE, settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' GMT+02:00'
            url = V2_Methods_Asis.ASIS_PAYPURSE_URL
            payload = {
                'header': {
                    'versionSchema': 1,
                    'clientSessionId': client_session_id,
                    'serverSessionId': server_session_id,
                    'dateTime': time_in_formatted,
                    'networkId': V2_Methods_Asis.ASIS_NETWORK_ID,
                },
                'content': {
                    'institutionCode': V2_Methods_Asis.ASIS_INSTITUTION_CODE,
                    'mediaFamily': 'MfrV2',
                    'mediaUniqueId': card_number,
                    # V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER, device.device_asis_serial_no
                    'deviceSerialNo': V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER,
                    'posNo': '',
                    'amount': amount,
                    'command': card_command,
                }
            }
            payload = json.dumps(payload)
            payload = str(payload)
            headers = {
                'Authorization': 'Bearer '+str(access_token),
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 31: API called failed from ASIS. Response: '+str(response), None

            # update card log
            card_log.card_log_web_top_up_request_body = payload
            card_log.card_log_web_top_up_response = result
            card_log.card_log_updated_at = Utils.get_current_datetime_utc()
            card_log.save()

            data = json.loads(result)
            if not data['result']:
                return True, 'Error 32: API called failed from ASIS. Response: '+str(data['message']), None
            message = data['result']['message']
            if message is not None:
                if message == 'Insufficient balance':
                    return True, 'Insufficient balance.', None
                return True, 'Error 33: API called failed from ASIS. Response: '+str(message), None
            return False, 'Success', data['content']
        except Exception as e:
            return True, 'Error 3: API called failed from ASIS. Response: '+str(e), None

    @classmethod
    def api_get_purse(cls, request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command, number=1):
        try:
            time_in_formatted = Utils.get_convert_datetime_other(
                Utils.get_current_datetime_utc(), settings.TIME_ZONE, settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' GMT+02:00'
            url = V2_Methods_Asis.ASIS_GETPURSE_URL
            payload = {
                'header': {
                    'versionSchema': 1,
                    'clientSessionId': client_session_id,
                    'serverSessionId': server_session_id,
                    'dateTime': time_in_formatted,
                    'networkId': V2_Methods_Asis.ASIS_NETWORK_ID,
                },
                'content': {
                    'institutionCode': V2_Methods_Asis.ASIS_INSTITUTION_CODE,
                    'mediaFamily': 'MfrV2',
                    'mediaUniqueId': card_number,
                    # V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER, device.device_asis_serial_no
                    'deviceSerialNo': V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER,
                    'posNo': '',
                    'amount': amount,
                    'command': card_command,
                }
            }
            payload = json.dumps(payload)
            payload = str(payload)
            headers = {
                'Authorization': 'Bearer '+str(access_token),
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 51: API called failed from ASIS. Response: '+str(response), None

            # update card log
            if number == 2:
                card_log.card_log_get_purse_2_request_body = payload
                card_log.card_log_get_purse_2_response = result
                card_log.card_log_updated_at = Utils.get_current_datetime_utc()
                card_log.save()
            else:
                card_log.card_log_get_purse_1_request_body = payload
                card_log.card_log_get_purse_1_response = result
                card_log.card_log_updated_at = Utils.get_current_datetime_utc()
                card_log.save()

            data = json.loads(result)
            if not data['result']:
                return True, 'Error 52: API called failed from ASIS. Response: '+str(data['message']), None
            message = data['result']['message']
            if message is not None:
                return True, 'Error 53: API called failed from ASIS. Response: '+str(message), None
            return False, 'Success', data['content']
        except Exception as e:
            return True, 'Error 5: API called failed from ASIS. Response: '+str(e), None

    @classmethod
    def api_end_session(cls, request, operator, device, card_log, access_token, server_session_id, card_number):
        try:
            time_in_formatted = Utils.get_convert_datetime_other(
                Utils.get_current_datetime_utc(), settings.TIME_ZONE, settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' GMT+02:00'

            url = V2_Methods_Asis.ASIS_END_SESSION_URL
            payload = {
                'header': {
                    # V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER, device.device_asis_serial_no
                    'deviceSerialNo': V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER,
                    'serverSessionId': server_session_id,
                    'status': time_in_formatted,
                },
                'content': {
                    'media': {
                        'mediaUniqueId': card_number,
                    }
                },
            }
            payload = json.dumps(payload)
            payload = str(payload)
            headers = {
                'Authorization': 'Bearer '+str(access_token),
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 41: API called failed from ASIS. Response: '+str(response), None

            card_log.card_log_end_session_request_body = payload
            card_log.card_log_end_session_response = result
            card_log.card_log_updated_at = Utils.get_current_datetime_utc()
            card_log.save()

            data = json.loads(result)
            if not data['result']:
                return True, 'Error 42: API called failed from ASIS. Response: '+str(data['message']), None
            message = data['result']['result']
            if message != "Success":
                return True, 'Error 43: API called failed from ASIS. Response: '+str(message), None
            return False, 'Success', data['result']['detail']
        except Exception as e:
            return True, 'Error 4: API called failed from ASIS. Response: '+str(e), None

    # start card payment session
    @classmethod
    def get_payment_session(cls, request, operator, device, card_number, amount):
        card_log = Card_Logs()
        card_log.card_log_card_number = card_number
        # V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER, device.device_asis_serial_no
        card_log.card_log_device_serial_number = V2_Methods_Asis.ASIS_DEVICE_SERIAL_NUMBER
        card_log.card_log_institution_code = V2_Methods_Asis.ASIS_INSTITUTION_CODE
        card_log.card_log_network_id = V2_Methods_Asis.ASIS_NETWORK_ID
        card_log.card_log_login_request_body = ''
        card_log.card_log_login_response = ''
        card_log.card_log_start_session_request_body = ''
        card_log.card_log_start_session_response = ''
        card_log.card_log_get_purse_1_request_body = ''
        card_log.card_log_get_purse_1_response = ''
        card_log.card_log_web_top_up_request_body = ''
        card_log.card_log_web_top_up_response = ''
        card_log.card_log_get_purse_2_request_body = ''
        card_log.card_log_get_purse_2_response = ''
        card_log.card_log_end_session_request_body = ''
        card_log.card_log_end_session_response = ''
        card_log.card_log_amount = 0
        card_log.card_log_old_balance = 0
        card_log.card_log_new_balance = 0
        card_log.card_log_response = ''
        card_log.card_log_created_at = Utils.get_current_datetime_utc()
        card_log.card_log_created_by = operator.operator_id
        card_log.card_log_updated_at = Utils.get_current_datetime_utc()
        card_log.card_log_updated_by = operator.operator_id
        card_log.save()

        error, message, access_token = V2_Methods_Asis.ap_login_token(
            request, card_log)
        if error:
            return error, message, None, None, None

        client_session_id = str(uuid.uuid1())
        error, message, session_data = V2_Methods_Asis.api_start_session(
            request, operator, device, card_log, access_token, client_session_id, card_number)
        if error:
            return error, message, None, None, None
        # server_session_id = data['header']['serverSessionId']
        return False, 'Success', access_token, session_data, card_log.card_log_id

    # process card payment main balance from ASIS
    @classmethod
    def process_payment(cls, request, operator, device, card_number, amount, card_command, access_token, session_data, card_log):
        client_session_id = session_data['header']['clientSessionId']
        server_session_id = session_data['header']['serverSessionId']

        # errorGet, messageGet, _ = V2_Methods_Asis.api_get_purse(
        #     request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command, number=1)
        # if errorGet:
        #     return errorGet, messageGet, None
        errorPay, messagePay, response_content = V2_Methods_Asis.api_pay_purse(
            request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command)
        error, message, _ = V2_Methods_Asis.api_end_session(
            request, operator, device, card_log, access_token, server_session_id, card_number)

        # update card log
        if errorPay:
            card_log.card_log_response = messagePay
            card_log.save()
        else:
            # if response_content['currentBalance'] >= get_response_content['balance']:
            #     return True, 'Unable to deduct money from card. Please retry again.', None

            card_log.card_log_response = messagePay
            card_log.card_log_amount = amount
            card_log.card_log_old_balance = response_content['previousBalance']
            card_log.card_log_new_balance = response_content['currentBalance']
            card_log.save()

        if errorPay:
            return errorPay, messagePay, None, card_log
        if error:
            return error, message, None, card_log

        return False, 'Success', response_content, card_log

    @classmethod
    def card_topup(cls, request, operator, card_number, amount):
        try:
            url = 'https://mobile-test.tapandgoticketing.co.rw/api/card/topup'
            payload = {
                'card_number': card_number,
                'pos_number': "00000000000000",
                'agent_username': operator.operator_username,
                'amount': amount,
            }
            payload = json.dumps(payload)
            headers = {
                'token': 'cp/}6dr;<#r2;9ZU6V}S/:"*H%h*4_@g',
                'Content-Type': 'application/json',
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 61: API called failed from Mobile Test. Response: '+str(response), None

            data = json.loads(result)
            error = data['error']
            if error:
                return True, 'Error 62: API called failed from Mobile Test. Response: '+str(data['message']), None

            return False, 'Success', data
        except Exception as e:
            return True, 'Error 6: API called failed from Mobile Test. Response: '+str(e), None
    
    @classmethod
    def get_card_balance(cls, request, operator, device, card_number, amount, card_command, access_token, session_data, card_log):
        client_session_id = session_data['header']['clientSessionId']
        server_session_id = session_data['header']['serverSessionId']
        errorGet, messageGet, get_response_content = V2_Methods_Asis.api_get_purse(
            request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command, number=1)
        if errorGet:
            return errorGet, messageGet, None
        balance = get_response_content['balance']
        
        card_log.card_log_response = messageGet
        card_log.card_log_amount = 0
        card_log.card_log_old_balance = 0
        card_log.card_log_new_balance = balance
        card_log.save()
        return False, 'Success', balance

    @classmethod
    def validate_card_topup(cls, request, operator, device, card_number, amount, card_command, access_token, session_data, card_log, transaction):
        client_session_id = session_data['header']['clientSessionId']
        server_session_id = session_data['header']['serverSessionId']

        errorGet, messageGet, get_response_content = V2_Methods_Asis.api_get_purse(
            request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command, number=1)
        if errorGet:
            return errorGet, messageGet, None

        balance = get_response_content['balance']
        if amount + balance > 40000:
            return True, 'Card topup '+str(amount + balance)+'('+str(balance)+'+'+str(amount)+') is exceeding 40,000 FRW.', None

        return False, 'Success', get_response_content

    @classmethod
    def process_card_topup(cls, request, operator, device, card_number, amount, card_command, access_token, session_data, card_log, get_response_content):
        client_session_id = session_data['header']['clientSessionId']
        server_session_id = session_data['header']['serverSessionId']

        # errorGet, messageGet, get_response_content = V2_Methods_Asis.api_get_purse(
        #     request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command, number=2)
        # if errorGet:
        #     return errorGet, messageGet, None

        errorPay, messagePay, response_content = V2_Methods_Asis.api_pay_purse(
            request, operator, device, card_log, access_token, client_session_id, server_session_id, card_number, amount, card_command)

        error, message, _ = V2_Methods_Asis.api_end_session(
            request, operator, device, card_log, access_token, server_session_id, card_number)

        # update card log
        if errorPay:
            card_log.card_log_response = messagePay
            card_log.save()
        else:
            card_log.card_log_response = messagePay
            card_log.card_log_amount = amount
            card_log.card_log_old_balance = response_content['previousBalance']
            card_log.card_log_new_balance = response_content['currentBalance']
            card_log.save()

        if errorPay:
            return errorPay, messagePay, None
        if error:
            return error, message, None

        return False, 'Success', response_content
