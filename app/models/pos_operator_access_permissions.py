from django.db import models

from app.models.operators import Operators
from app.models.pos_access_permissions import Pos_Access_Permissions


class Pos_Operator_Access_Permissions(models.Model):
    pos_operator_access_permission_id = models.AutoField('Id', primary_key=True)
    pos_operator_access_permission_name = models.CharField(
        'Name', max_length=255, blank=False, default='')
    pos_operator_access_permission_operator_id = models.IntegerField(
        'Operator', blank=False, default=0)
    pos_operator_access_permission_created_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    pos_operator_access_permission_updated_at = models.IntegerField(
        'Updated By', blank=False, default=0)

    class Meta:
        db_table = "pos_operator_access_permissions"
