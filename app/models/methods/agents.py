from app.models.companies import Companies
from app.models.agent_deployments import Agent_Deployments
import os
import json
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from app import settings
from app.models import Agents, Operators
from app.utils import Utils


class Methods_Agents():
    @classmethod
    def format_view(cls, request, operator, model):

        try:
            agent = Agents.objects.get(
                pk=model.agent_supervisor)
            model.agent_supervisor = mark_safe(
                '<a href=' + reverse("agents_view",
                                     args=[agent.agent_id]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(agent.agent_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            model.agent_supervisor = 'None'

        agent_deployments = Agent_Deployments.objects.filter(
                agent_deployment_agent_id=model.agent_id).order_by('-agent_deployment_id')
        model.agent_company = 'N/A'
        if agent_deployments.count() > 0:
            agent_deployment = agent_deployments[0]
            try:
                company = Companies.objects.get(
                        pk=agent_deployment.agent_deployment_company_id)
                model.agent_company = company.company_name
            except(TypeError, ValueError, OverflowError, Companies.DoesNotExist):
                model.agent_company = 'N/A'

        model.agent_created_at = Utils.get_convert_datetime(model.agent_created_at,
                                                            settings.TIME_ZONE,
                                                            settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.agent_updated_at = Utils.get_convert_datetime(model.agent_updated_at,
                                                            settings.TIME_ZONE,
                                                            settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

        try:
            operator = Operators.objects.get(
                pk=model.agent_created_by)
            model.agent_created_by = str(
                operator.operator_first_name) + ' ' + str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.agent_updated_by)
            model.agent_updated_by = str(
                operator.operator_first_name) + ' ' + str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        return model

    @classmethod
    def format_input(cls, request):
        return {
        }

    @classmethod
    def form_view(cls, request, operator, model, api=False):
        return {
            'id': model.agent_id,
            'nida': model.agent_nid,
            'username': model.agent_username,
            'name': model.agent_name,
            'email': model.agent_email_id,
            'phone': model.agent_phone_number,
            'supervisor': model.agent_supervisor,
            'balance_card': model.agent_balance_card,
            'payment_token': model.agent_payment_token,
        }

    @classmethod
    def validate(cls, request, operator, model, new=False):
        # username
        try:
            exists = Agents.objects.get(
                agent_username=model.agent_username)
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            exists = None
        if exists is not None and exists.agent_id != model.agent_id:
            return True, 'Username is already in use.', model

        # nida
        try:
            exists = Agents.objects.get(
                agent_nid=model.agent_nid)
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            exists = None
        if exists is not None and exists.agent_id != model.agent_id:
            return True, 'NIDA ID is already in use.', model

        # payment token
        try:
            exists = Agents.objects.get(
                agent_payment_token=model.agent_payment_token)
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            exists = None
        if exists is not None and exists.agent_id != model.agent_id:
            return True, 'Payment token is already in use.', model

        return False, 'Success', model

    @classmethod
    def update_status(cls, request, operator, model, status, action=None, data=None):
        model.agent_updated_at = Utils.get_current_datetime_utc()
        model.agent_updated_by = operator.operator_id
        model.agent_status = status

        model.save()
        return model
