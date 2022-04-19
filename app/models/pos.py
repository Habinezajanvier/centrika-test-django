from django.db import models
from app import settings
from app.models.companies import Companies


class Pos(models.Model):
    TITLE = settings.MODEL_POS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_POS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    pos_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    pos_company_id = models.IntegerField(
        'Company', blank=False, default=0)
    pos_serial_number = models.CharField(
        'Serial Number', max_length=255, blank=False, unique=True)
    pos_app_version_no = models.IntegerField(
        'App Version', blank=False, default=0)
    pos_app_version_name = models.CharField(
        'App Version Name', max_length=255, blank=False, default='')
    pos_agent_id = models.IntegerField(
        'Agent', blank=False, default=0)
    pos_asis_device_serial_number = models.CharField(
        'Asis Device Serial Number', max_length=255, blank=False, default='')
    pos_push_key = models.CharField(
        'Push Key', max_length=255, blank=False, default='')
    pos_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    pos_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    pos_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    pos_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    pos_status = models.IntegerField(
        'Status', blank=False, default=Companies.STATUS_ACTIVE)

    class Meta:
        db_table = "pos"

    def __unicode__(self):
        return self.pos_id
