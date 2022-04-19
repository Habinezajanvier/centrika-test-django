

from django.urls.base import reverse
from django.utils.safestring import mark_safe
from django.db import models
from app import settings
from app.utils import Utils
from app.models.operators import Operators

class Methods_Tickets_External():
    @classmethod
    def format_view(cls, request, operator, model):
        if model.ticket_requested_at != 0:
            model.ticket_requested_at = Utils.get_convert_datetime(model.ticket_requested_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO
        if model.ticket_confirmed_at != 0:      
            model.ticket_confirmed_at = Utils.get_convert_datetime(model.ticket_confirmed_at,
                                                               settings.TIME_ZONE,
                                                               settings.APP_CONSTANT_DISPLAY_TIME_ZONE) + ' ' + settings.APP_CONSTANT_DISPLAY_TIME_ZONE_INFO

        return model
