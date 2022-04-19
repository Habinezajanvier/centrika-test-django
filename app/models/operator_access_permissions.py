from django.db import models

from app.models.operators import Operators
from app.models.access_permissions import Access_Permissions


class Operator_Access_Permissions(models.Model):
    operator_access_permission_id = models.AutoField('Id', primary_key=True)
    operator_access_permission_name = models.CharField(
        'Name', max_length=255, blank=False, default='')
    operator_access_permission_operator_id = models.IntegerField(
        'Operator', blank=False, default=0)
    operator_access_permission_created_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    operator_access_permission_updated_at = models.IntegerField(
        'Updated By', blank=False, default=0)

    class Meta:
        db_table = "operator_access_permissions"
