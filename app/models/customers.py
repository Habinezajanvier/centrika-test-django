from decimal import Decimal
from django.db import models


class Customers(models.Model):
    customer_id = models.AutoField('Id', primary_key=True)
    customer_phone_number = models.CharField(
        'Phone', max_length=13, blank=False, unique=True)
    customer_name = models.CharField(
        'Name', max_length=255, blank=False)
    customer_email_id = models.EmailField(
        'Email id', max_length=100, blank=True)
    customer_balance = models.DecimalField('Balance', max_digits=30, decimal_places=2,
                                           default=Decimal(0.0))
    customer_nid = models.CharField(
        'NID', max_length=100, blank=False, default='')
    customer_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    customer_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    customer_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    customer_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    customer_status = models.IntegerField(
        'Status', blank=False, default=1)

    class Meta:
        db_table = "customers"

    def __unicode__(self):
        return self.customer_id
