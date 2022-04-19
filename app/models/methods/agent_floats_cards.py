import json
import os
import uuid
import requests

from app import settings
from app.models import Agents, Operators
from app.models.agent_floats_cards import Agent_Floats_Cards
from app.models.companies import Companies
from app.models.methods.api_requests import Methods_Api_Requests
from app.utils import Utils
from django.contrib.auth.hashers import make_password
from django.db import connection, models
from django.db.models import Q
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)


class Methods_Agent_Floats_Cards():

    @classmethod
    def format_view(cls, request, operator, model):
        try:
            agent = Agents.objects.get(
                pk=model.agent_float_agent_id)
            model.agent_float_agent_id = mark_safe(
                '<a href=' + reverse("agents_view",
                                     args=[agent.agent_id]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(agent.agent_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            model.agent_float_agent_id = 'None'

        try:
            company = Companies.objects.get(
                pk=model.agent_float_company_id)
            model.agent_float_company_id = str(company.company_name)
        except(TypeError, ValueError, OverflowError, Companies.DoesNotExist):
            model.agent_float_company_id = 'None'

        model.agent_float_requested_at = Utils.get_convert_datetime(model.agent_float_requested_at,
                                                                    settings.TIME_ZONE,
                                                                    settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        if model.agent_float_approval_updated_at != 0:
            model.agent_float_approval_updated_at = Utils.get_convert_datetime(model.agent_float_approval_updated_at,
                                                                               settings.TIME_ZONE,
                                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        else:
            model.agent_float_approval_updated_at = None

        if model.agent_float_requested_md == 0:
            try:
                item = Operators.objects.get(
                    pk=model.agent_float_requested_by)
                model.agent_float_requested_by = str(item.operator_first_name) +' '+str(item.operator_last_name)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                print('')
        
        if model.agent_float_requested_md == 1:
            try:
                agent = Agents.objects.get(
                    pk=model.agent_float_requested_by)
                model.agent_float_requested_by = agent.agent_name
            except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
                print('')
        
        if model.agent_float_approval_updated_md == 0:
            try:
                item = Operators.objects.get(
                    pk=model.agent_float_approval_updated_by)
                model.agent_float_approval_updated_by = str(item.operator_first_name) +' '+str(item.operator_last_name)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                print('')

        if model.agent_float_approval_updated_md == 1:
            try:
                agent = Agents.objects.get(
                    pk=model.agent_float_approval_updated_by)
                model.agent_float_approval_updated_by = agent.agent_name
            except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
                print('')

        return model

    @classmethod
    def format_input(cls, request):
        return {
        }

    @classmethod
    def form_view(cls, request, operator, model, api=False):
        if api:
            try:
                company = Companies.objects.get(
                    pk=model.agent_float_company_id)
                model.agent_float_company_id = str(company.company_name)
            except(TypeError, ValueError, OverflowError, Companies.DoesNotExist):
                model.agent_float_company_id = 'N/A'
            model.agent_float_requested_at = Utils.get_convert_datetime(model.agent_float_requested_at,
                                                                        settings.TIME_ZONE,
                                                                        settings.APP_CONSTANT_DISPLAY_TIME_ZONE)
            if model.agent_float_approval_updated_at != 0:
                model.agent_float_approval_updated_at = Utils.get_convert_datetime(model.agent_float_approval_updated_at,
                                                                                   settings.TIME_ZONE,
                                                                                   settings.APP_CONSTANT_DISPLAY_TIME_ZONE)
            else:
                model.agent_float_approval_updated_at = 'N/A'
            
            if model.agent_float_requested_md == 0:
                try:
                    item = Operators.objects.get(
                        pk=model.agent_float_requested_by)
                    model.agent_float_requested_by = str(item.operator_first_name) +' '+str(item.operator_last_name)
                except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                    model.agent_float_requested_by = 'N/A'
            
            if model.agent_float_requested_md == 1:
                try:
                    agent = Agents.objects.get(
                        pk=model.agent_float_requested_by)
                    model.agent_float_requested_by = agent.agent_name
                except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
                    model.agent_float_requested_by = 'N/A'
            
            if model.agent_float_approval_updated_md == 0:
                try:
                    item = Operators.objects.get(
                        pk=model.agent_float_approval_updated_by)
                    model.agent_float_approval_updated_by = str(item.operator_first_name) +' '+str(item.operator_last_name)
                except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                    model.agent_float_approval_updated_by = 'N/A'

            if model.agent_float_approval_updated_md == 1:
                try:
                    agent = Agents.objects.get(
                        pk=model.agent_float_approval_updated_by)
                    model.agent_float_approval_updated_by = agent.agent_name
                except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
                    model.agent_float_approval_updated_by = 'N/A'
                    
            return {
                'id': model.agent_float_id,
                'type': model.agent_float_type,
                'bill': model.agent_float_bill,
                'action': model.agent_float_action,
                'action_id': model.agent_float_action_id,
                'refund': model.agent_float_action_refund,
                'refund_id': model.agent_float_action_refund_id,
                'amount': model.agent_float_amount,
                'old_balance': model.agent_float_old_balance,
                'new_balance': model.agent_float_new_balance,
                'card': model.agent_float_card_number,
                'card_old_balance': model.agent_float_card_old_balance,
                'card_new_balance': model.agent_float_card_new_balance,
                'customer_name': model.agent_float_customer_name,
                'customer_phone_number': model.agent_float_customer_phone_number,
                'company': model.agent_float_company_id,
                'requested_at': model.agent_float_requested_at,
                'requested_by': model.agent_float_requested_by,
                'approval_updated_at': model.agent_float_approval_updated_at,
                'approval_updated_by': model.agent_float_approval_updated_by,
                'status': model.agent_float_status,
                'bank_reference': model.agent_float_bank_reference,
            }

        return {
            'id': model.agent_float_id,
            'agent': model.agent_float_agent_id,
            'type': model.agent_float_type,
            'bill': model.agent_float_bill,
            'amount': model.agent_float_amount,
            'old_balance': model.agent_float_old_balance,
            'new_balance': model.agent_float_new_balance,
            'reason': model.agent_float_reason,
            'action': model.agent_float_action,
            'action_id': model.agent_float_action_id,
            'refund': model.agent_float_action_refund,
            'refund_id': model.agent_float_action_refund_id,
            'bank_reference': model.agent_float_bank_reference,
        }

    @classmethod
    def validate(cls, request, operator, model, new=False):
        return False, 'Success', model

    @classmethod
    def add(cls, request, operator, agent, data, model=None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Agent_Floats_Cards()

        model.agent_float_agent_id = agent.agent_id
        model.agent_float_agent_name = agent.agent_name
        model.agent_float_type = Agent_Floats_Cards.TYPE_ADD
        model.agent_float_bill = None
        model.agent_float_amount = data['amount']
        model.agent_float_old_balance = 0
        model.agent_float_new_balance = 0
        model.agent_float_reason = data['reason']
        model.agent_float_action = data['action']
        model.agent_float_action_id = 0
        model.agent_float_action_refund = 0
        model.agent_float_action_refund_id = 0
        model.agent_float_ticket_id = 0
        model.agent_float_company_id = 0
        model.agent_float_company_name = ''
        model.agent_float_transaction_id = 0
        model.agent_float_card_id = 0
        model.agent_float_card_number = ''
        model.agent_float_card_old_balance = ''
        model.agent_float_card_new_balance = ''
        model.agent_float_customer_id = 0
        model.agent_float_customer_name = ''
        model.agent_float_customer_phone_number = ''
        model.agent_float_requested_at = Utils.get_current_datetime_utc()
        model.agent_float_requested_by = agent.agent_id
        model.agent_float_requested_md = 1
        model.agent_float_requested_by_name = agent.agent_name
        model.agent_float_approval_updated_at = 0
        model.agent_float_approval_updated_by = 0
        model.agent_float_approval_updated_md = 1
        model.agent_float_approval_updated_by_name = ''
        model.agent_float_status = Agent_Floats_Cards.STATUS_PENDING
        model.agent_float_bank_reference = ''
        model.save()
        return False, 'Success', model
    
    @classmethod
    def add_bill(cls, request, operator, agent, data, model=None):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            return True, 'Not found.', model
        
        bill = None
        try:
            url = settings.FMS_BANK_API_URL + "/v7/agent-floats-bank/add-request"
            payload = json.dumps({
                "agent_float_instance_id": settings.FMS_BANK_INSTANCE_ID,
                "agent_float_id": model.agent_float_id,
                "agent_float_agent_id": model.agent_float_agent_id,
                "agent_float_agent_name": model.agent_float_agent_name,
                "agent_float_type": model.agent_float_type,
                "agent_float_bill": model.agent_float_bill,
                "agent_float_old_balance": model.agent_float_old_balance,
                "agent_float_new_balance": model.agent_float_new_balance,
                "agent_float_reason": model.agent_float_reason,
                "agent_float_action": model.agent_float_action,
                "agent_float_action_id": model.agent_float_action_id,
                "agent_float_action_refund": model.agent_float_action_refund,
                "agent_float_action_refund_id": model.agent_float_action_refund_id,
                "agent_float_ticket_id": model.agent_float_ticket_id,
                "agent_float_company_id": model.agent_float_company_id,
                "agent_float_company_name": model.agent_float_company_name,
                "agent_float_transaction_id": model.agent_float_transaction_id,
                "agent_float_card_id": model.agent_float_card_id,
                "agent_float_card_number": model.agent_float_card_number,
                "agent_float_card_old_balance": model.agent_float_card_old_balance,
                "agent_float_card_new_balance": model.agent_float_card_new_balance,
                "agent_float_customer_id": model.agent_float_customer_id,
                "agent_float_customer_name": model.agent_float_customer_name,
                "agent_float_customer_phone_number": model.agent_float_customer_phone_number,
                "agent_float_requested_at": model.agent_float_requested_at,
                "agent_float_requested_by": model.agent_float_requested_by,
                "agent_float_requested_md": model.agent_float_requested_md,
                "agent_float_requested_by_name": model.agent_float_requested_by_name,
                "agent_float_approval_updated_at": model.agent_float_approval_updated_at,
                "agent_float_approval_updated_by": model.agent_float_approval_updated_by,
                "agent_float_approval_updated_md": model.agent_float_approval_updated_md,
                "agent_float_approval_updated_by_name": model.agent_float_approval_updated_by_name,
                "agent_float_status": model.agent_float_status,
                "agent_float_bank_reference": "",
            })
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response)
            try:
                result = (response.content).decode("utf-8")
            except(TypeError, ValueError, OverflowError, UnicodeDecodeError):
                return True, 'Error 1: Unable to generate unique reference number. Response: '+str(response), None
            data = json.loads(result)
            if data['error']:
                return True, 'Error 2: Unable to generate unique reference number. Response: '+str(response), None
            bill = data['data']['agent_float_bill']
        except Exception as e:
            return True, 'Error 3: Unable to generate unique reference number. Response: '+str(e), None
        
        model.agent_float_bill = bill
        model.save()
        return False, 'Success', model

    @classmethod
    def remove(cls, request, operator, agent, data, model=None, card=None, company=None, card_number=''):
        data = json.dumps(data)
        data = json.loads(data)

        if model is None:
            model = Agent_Floats_Cards()

        if agent.agent_balance_card < data['amount']:
            return True, 'Insufficient balance.', model

        model.agent_float_agent_id = agent.agent_id
        model.agent_float_agent_name = agent.agent_name
        model.agent_float_type = Agent_Floats_Cards.TYPE_REMOVE
        model.agent_float_bill = None
        model.agent_float_amount = data['amount']
        model.agent_float_old_balance = agent.agent_balance_card
        model.agent_float_new_balance = agent.agent_balance_card - data['amount']
        model.agent_float_reason = data['reason']
        model.agent_float_action = data['action']
        model.agent_float_action_id = int(data['action_id'])
        model.agent_float_action_refund = int(data['refund'])
        model.agent_float_action_refund_id = int(data['refund_id'])
        model.agent_float_ticket_id = 0
        if card is None:
            if company is None:
                model.agent_float_company_id = 0
                model.agent_float_company_name = ''
            else:
                model.agent_float_company_id = company.company_id
                model.agent_float_company_name = company.company_name
            model.agent_float_transaction_id = 0
            model.agent_float_card_id = 0
            model.agent_float_card_number = card_number
            model.agent_float_card_old_balance = ''
            model.agent_float_card_new_balance = ''
            model.agent_float_customer_id = 0
            model.agent_float_customer_name = ''
            model.agent_float_customer_phone_number = ''
        else:
            if company is None:
                model.agent_float_company_id = 0
                model.agent_float_company_name = ''
            else:
                model.agent_float_company_id = company.company_id
                model.agent_float_company_name = company.company_name
            model.agent_float_transaction_id = 0
            model.agent_float_card_id = card.card_id
            model.agent_float_card_number = card.card_number
            model.agent_float_card_old_balance = ''
            model.agent_float_card_new_balance = ''
            model.agent_float_customer_id = 0
            model.agent_float_customer_name = ''
            model.agent_float_customer_phone_number = ''
        model.agent_float_requested_at = Utils.get_current_datetime_utc()
        model.agent_float_requested_by = agent.agent_id
        model.agent_float_requested_md = 1
        model.agent_float_requested_by_name = agent.agent_name
        model.agent_float_approval_updated_at = Utils.get_current_datetime_utc()
        model.agent_float_approval_updated_by = agent.agent_id
        model.agent_float_approval_updated_md = 1
        model.agent_float_approval_updated_by_name = agent.agent_name
        model.agent_float_status = Agent_Floats_Cards.STATUS_APPROVED
        model.agent_float_bank_reference = ''
        model.save()
        agent.agent_balance_card = model.agent_float_new_balance
        agent.save()
        return False, 'Success', model

    @classmethod
    def update_status(cls, request, operator, agent, model, status, action=None, data=None, system_agent=None, sub_agent=None):
        model.agent_float_approval_updated_at = Utils.get_current_datetime_utc()
        if system_agent is None:
            model.agent_float_approval_updated_by = 0
            if operator is not None:
                model.agent_float_approval_updated_md = 0
                model.agent_float_approval_updated_by = operator.operator_id
        else:
            model.agent_float_approval_updated_by = system_agent.agent_id
        model.agent_float_status = status
        if sub_agent is not None:
            if status == Agent_Floats_Cards.STATUS_APPROVED:
                model.agent_float_old_balance = sub_agent.agent_balance_card
                model.agent_float_new_balance = sub_agent.agent_balance_card + model.agent_float_amount
                model.save()
                sub_agent.agent_balance_card = model.agent_float_new_balance
                sub_agent.save()
            if status == Agent_Floats_Cards.STATUS_DENIED:
                model.save()
        else:
            if status == Agent_Floats_Cards.STATUS_APPROVED:
                model.agent_float_old_balance = agent.agent_balance_card
                model.agent_float_new_balance = agent.agent_balance_card + model.agent_float_amount
                model.save()
                agent.agent_balance_card = model.agent_float_new_balance
                agent.save()
            if status == Agent_Floats_Cards.STATUS_DENIED:
                model.save()
        return model

    @classmethod
    def get_agent_floats_history_pending(cls, request, operator, agent, date):
        if agent.agent_supervisor == 0:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_status=Agent_Floats_Cards.STATUS_PENDING)
            )
        else:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_agent_id=agent.agent_id) &
                Q(agent_float_status=Agent_Floats_Cards.STATUS_PENDING)
            )
        seconds = (Utils.convert_string_to_datetime(date+' 00:00:00')
                   ).timestamp() + settings.TIME_DIFFERENCE
        objects = objects.filter(
            Q(agent_float_requested_at__gte=seconds) &
            Q(agent_float_requested_at__lt=(seconds+86400))
        )
        float_transactions = objects.all().order_by('-agent_float_id')
        list_floats_transactions_by_agent = []
        for float_transaction in float_transactions:
            list_floats_transactions_by_agent.append(
                Methods_Agent_Floats_Cards.form_view(
                    request, operator, float_transaction, True)
            )

        return list_floats_transactions_by_agent

    @classmethod
    def get_agent_floats_history_approved(cls, request, operator, agent, date):
        if agent.agent_supervisor == 0:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_status=Agent_Floats_Cards.STATUS_APPROVED)
            )
        else:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_agent_id=agent.agent_id) &
                Q(agent_float_status=Agent_Floats_Cards.STATUS_APPROVED)
            )
        seconds = (Utils.convert_string_to_datetime(date+' 00:00:00')
                   ).timestamp() + settings.TIME_DIFFERENCE
        objects = objects.filter(
            Q(agent_float_approval_updated_at__gte=seconds) &
            Q(agent_float_approval_updated_at__lt=(seconds+86400))
        )
        float_transactions = objects.all().order_by('-agent_float_id')
        list_floats_transactions_by_agent = []
        for float_transaction in float_transactions:
            list_floats_transactions_by_agent.append(
                Methods_Agent_Floats_Cards.form_view(
                    request, operator, float_transaction, True)
            )

        return list_floats_transactions_by_agent

    @classmethod
    def get_agent_floats_history_denied(cls, request, operator, agent, date):
        if agent.agent_supervisor == 0:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_status=Agent_Floats_Cards.STATUS_DENIED)
            )
        else:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_agent_id=agent.agent_id) &
                Q(agent_float_status=Agent_Floats_Cards.STATUS_DENIED)
            )
        seconds = (Utils.convert_string_to_datetime(date+' 00:00:00')
                   ).timestamp() + settings.TIME_DIFFERENCE
        objects = objects.filter(
            Q(agent_float_approval_updated_at__gte=seconds) &
            Q(agent_float_approval_updated_at__lt=(seconds+86400))
        )
        float_transactions = objects.all().order_by('-agent_float_id')
        list_floats_transactions_by_agent = []
        for float_transaction in float_transactions:
            list_floats_transactions_by_agent.append(
                Methods_Agent_Floats_Cards.form_view(
                    request, operator, float_transaction, True)
            )

        return list_floats_transactions_by_agent

    @classmethod
    def get_agent_floats_history(cls, request, operator, agent, date, card_number, float_add, float_add_refund, float_transfer, float_transfer_refund, float_topup, float_topup_refund, status_pending, status_approved, status_declined):
        if agent.agent_supervisor == 0:
            objects = Agent_Floats_Cards.objects
        else:
            objects = Agent_Floats_Cards.objects.filter(
                Q(agent_float_agent_id=agent.agent_id)
            )
        seconds = (Utils.convert_string_to_datetime(date+' 00:00:00')
                   ).timestamp() + settings.TIME_DIFFERENCE
        objects = objects.filter(
            Q(agent_float_requested_at__gte=seconds) &
            Q(agent_float_requested_at__lt=(seconds+86400))
        )
        if card_number != '':
            objects = objects.filter(
                Q(agent_float_card_number=card_number)
            )
        float_actions = []
        if float_add:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_DEFAULT)
        if float_add_refund:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_DEFAULT_REFUND)
        if float_transfer:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_TRANSFER)
        if float_transfer_refund:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_TRANSFER_REFUND)
        if float_topup:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_CARD_TOPUP)
        if float_topup_refund:
            float_actions.append(Agent_Floats_Cards.TEXT_ACTION_CARD_TOPUP_REFUND)
        objects = objects.filter(
                Q(agent_float_action__in=float_actions))
        float_status = []
        if status_pending:
            float_status.append(Agent_Floats_Cards.STATUS_PENDING)
        if status_approved:
            float_status.append(Agent_Floats_Cards.STATUS_APPROVED)
        if status_declined:
            float_status.append(Agent_Floats_Cards.STATUS_DENIED)
        objects = objects.filter(
                Q(agent_float_status__in=float_status))

        queryset = objects.all()
        float_transactions = queryset.order_by('-agent_float_id')
        # response = {
        #     "error": False,
        #     "message": 'Success',
        #     "data": {
        #         'query': queryset.query.__str__(),
        #     },
        # }
        # Methods_Api_Requests.addV2(request, 0, {
        #                          'action': 'agent-transactions', 'status': HTTP_200_OK, 'response': response})
        list_floats_transactions_by_agent = []
        for float_transaction in float_transactions:
            list_floats_transactions_by_agent.append(
                Methods_Agent_Floats_Cards.form_view(
                    request, operator, float_transaction, True)
            )

        return list_floats_transactions_by_agent
