from django.db import models

from app.models.operators import Operators
from app.models.access_permissions import Access_Permissions


class Operator_Access_Permissions(models.Model):
    operator_access_permission_id = models.AutoField('Id', primary_key=True)
    operators_operator_id = models.ForeignKey(
        Operators, on_delete=models.CASCADE)
    access_permissions_access_permission_name = models.ForeignKey(
        Access_Permissions, on_delete=models.CASCADE)
    operator_access_permission_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    operator_access_permission_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
