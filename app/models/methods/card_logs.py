

from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.db import models
from app import settings
from app.utils import Utils
from operators import Operators


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
            operator = Operators.objects.get(
                pk=model.card_log_created_by)
            model.card_log_created_by = str(operator.operator_first_name) + ' ' +str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        try:
            operator = Operators.objects.get(
                pk=model.card_log_updated_by)
            model.card_log_updated_by = str(operator.operator_first_name) + ' ' +str(operator.operator_last_name)
        except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
            print('')

        return model
