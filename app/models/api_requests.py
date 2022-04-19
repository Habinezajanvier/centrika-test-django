from django.db import models

from app import settings

class Api_Requests(models.Model):
    TITLE = settings.MODEL_CARDS_LOGS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_CARDS_LOGS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    api_version = models.CharField(
        'Api Version', max_length=255, blank=True)
    api_controller = models.CharField(
        'Api Controller', max_length=255, blank=True)
    api_action = models.CharField(
        'Api Action', max_length=255, blank=True)
    app_type = models.CharField(
        'App Type', max_length=255, blank=True)
    app_version = models.CharField(
        'Api Version', max_length=255, blank=True)
    app_device = models.CharField(
        'Device', max_length=255, blank=True)
    app_device_id = models.CharField(
        'Device Id', max_length=255, blank=True)
    app_device_os = models.CharField(
        'Device OS', max_length=255, blank=True)
    request_url = models.CharField(
        'Request Url', max_length=255, blank=True)
    request_header = models.TextField(
        'Request Header', blank=True)
    request_body = models.TextField(
        'Request Body', blank=True)
    requested_at = models.IntegerField(
        'Requested At', blank=False, default=0)
    requested_by = models.IntegerField(
        'Requested By', blank=False, default=0)
    response_status = models.CharField(
        'Status', max_length=255, blank=True)
    response_body = models.TextField(
        'Response Body', blank=True)
    browser = models.CharField(
        'Browser', max_length=255, blank=True)
    ip_address = models.CharField(
        'Ip Address', max_length=255, blank=True)

    class Meta:
        db_table = "api_requests"

    def __unicode__(self):
        return self.id
