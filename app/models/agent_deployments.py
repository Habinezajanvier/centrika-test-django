from django.db import models
from decimal import Decimal

from app import settings


class Agent_Deployments(models.Model):
    agent_deployment_id = models.AutoField(
        'Id', primary_key=True)
    agent_deployment_agent_id = models.IntegerField(
        'Agent', blank=False, default=0)
    agent_deployment_company_id = models.IntegerField(
        'Company', blank=False, default=0)
    agent_deployment_company_branch_id = models.IntegerField(
        'Branch', blank=False, default=0)

    agent_deployment_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    agent_deployment_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    agent_deployment_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    agent_deployment_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    agent_deployment_status = models.IntegerField(
        'Status', blank=False, default=1)

    class Meta:
        db_table = "agent_deployments"
