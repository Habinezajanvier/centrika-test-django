

import json
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from app.models.api_requests import Api_Requests
from django.db import models
from app import settings
from app.utils import Utils
from django.core import serializers


class Methods_Api_Requests():
    @classmethod
    def add(cls, request, agent_id, data):
        api_request = Api_Requests()
        api_request.api_version = "v18"
        api_request.api_controller = "ApiController"
        api_request.api_action = data.get('action')
        api_request.app_type = "None"
        api_request.app_version = "v18"
        api_request.app_device = ""
        api_request.app_device_id = "0"
        api_request.app_device_os = "Android"
        api_request.request_url = "{0}://{1}{2}".format(
            request.scheme, request.get_host(), request.path)
        api_request.request_header = json.dumps(dict(request.headers))
        api_request.request_body = request.body
        api_request.response_status = data.get('status')
        api_request.response_body = data.get('response')
        api_request.browser = Utils.get_browser_details_from_request(request)
        api_request.ip_address = Utils.get_ip_address(request)
        api_request.requested_at = Utils.get_current_datetime_utc()
        api_request.requested_by = agent_id
        api_request.save()
        return api_request

    @classmethod
    def addV2(cls, request, agent_id, data):
        api_request = Api_Requests()
        api_request.api_version = "v18"
        api_request.api_controller = "ApiController"
        api_request.api_action = data.get('action')
        api_request.app_type = "None"
        api_request.app_version = "v18"
        api_request.app_device = ""
        api_request.app_device_id = "0"
        api_request.app_device_os = "Android"
        api_request.request_url = "{0}://{1}{2}".format(
            request.scheme, request.get_host(), request.path)
        api_request.request_header = json.dumps(dict(request.headers))
        api_request.request_body = request.data
        api_request.response_status = data.get('status')
        api_request.response_body = data.get('response')
        api_request.browser = Utils.get_browser_details_from_request(request)
        api_request.ip_address = Utils.get_ip_address(request)
        api_request.requested_at = Utils.get_current_datetime_utc()
        api_request.requested_by = agent_id
        api_request.save()
        return api_request
