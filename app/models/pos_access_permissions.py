from django.db import models


class Pos_Access_Permissions(models.Model):
    pos_access_permission_name = models.CharField('Pos Access Permission Name', primary_key=True, max_length=255, blank=False,
                                              unique=True)
    pos_access_permission_details = models.CharField(
        'Details', max_length=255, blank=True)
    pos_access_permission_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    pos_access_permission_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    
    class Meta:
        db_table = "pos_access_permissions"
