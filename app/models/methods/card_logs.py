

from django.urls.base import reverse
from django.utils.safestring import mark_safe
from app.models.agents import Agents
from django.db import models
from app import settings
from app.utils import Utils


class Methods_Card_Logs():
    @classmethod
    def format_view(cls, request, operator, model):
        model.card_log_created_at = Utils.get_convert_datetime(model.card_log_created_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        model.card_log_updated_at = Utils.get_convert_datetime(model.card_log_updated_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

        try:
            agent = Agents.objects.get(
                pk=model.card_log_created_by)
            model.card_log_created_by = mark_safe(
                '<a href=' + reverse("agents_view",
                                     args=[agent.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(agent.agent_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            print('')

        try:
            agent = Agents.objects.get(
                pk=model.card_log_updated_by)
            model.card_log_updated_by = mark_safe(
                '<a href=' + reverse("agents_view",
                                     args=[agent.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                str(agent.agent_name) + '</a>')
        except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
            print('')

        return model
