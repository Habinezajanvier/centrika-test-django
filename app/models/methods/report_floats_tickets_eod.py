

from app.models.agent_floats_tickets import Agent_Floats_Tickets
from django.conf import settings
from django.db.models.aggregates import Sum
from django.db.models import Q


class Report_Floats_Tickets_EOD():
    @staticmethod
    def get_data_by_values(request, operator, filter_form, filter_date, filter_agent, filter_company=-1, filter_status=-1, refund=False, balance = False):
        objects = Agent_Floats_Tickets.objects
        if filter_status >= 0:
            objects = objects.filter(
                Q(agent_float_status=filter_status))
        if not balance:
            if refund:
                objects = objects.filter(
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_DEFAULT_REFUND) |
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_TRANSFER_REFUND)
                )
            else:
                objects = objects.filter(
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_DEFAULT) |
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_TRANSFER)
                )
                
        if filter_date != '' and filter_date is not None:
            objects = objects.filter(
                Q(agent_float_requested_at__gte=filter_date))
            objects = objects.filter(
                Q(agent_float_requested_at__lt=filter_date+86400))
        if filter_agent != '' and filter_agent != '-1':
            objects = objects.filter(
                Q(agent_float_requested_by=filter_agent))
        if filter_company != '' and filter_company != '-1':
            objects = objects.filter(
                Q(agent_float_company_id=filter_company))

        if balance:
            agent_float_old_balance = 0
            agent_float_new_balance = 0
            if filter_status == Agent_Floats_Tickets.STATUS_APPROVED:
                objects_first = objects_last = objects
                first = objects_first.all().first()
                if first is not None:
                    agent_float_old_balance = first.agent_float_old_balance
                last = objects_last.all().last()
                if last is not None:
                    agent_float_new_balance = last.agent_float_new_balance
            return agent_float_old_balance, agent_float_new_balance

        amount = int(objects.all().aggregate(
            Sum('agent_float_amount'))['agent_float_amount__sum'] or 0)
        count = objects.count()
        return amount, count

    @staticmethod
    def get_data(request, operator, filter_form, filter_status=-1, refund=False, balance = False):
        filter_date = filter_form.cleaned_data['date']
        if filter_date != '' and filter_date is not None:
            filter_date = int(filter_date.strftime(
                '%s')) + settings.TIME_DIFFERENCE
        filter_agent = filter_form.cleaned_data['agent']
        filter_company = filter_form.cleaned_data['company']
        objects = Agent_Floats_Tickets.objects
        if filter_status >= 0:
            objects = objects.filter(
                Q(agent_float_status=filter_status))
        if not balance:
            if refund:
                objects = objects.filter(
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_DEFAULT_REFUND) |
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_TRANSFER_REFUND)
                )
            else:
                objects = objects.filter(
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_DEFAULT) |
                    Q(agent_float_action=Agent_Floats_Tickets.TEXT_ACTION_TRANSFER)
                )
        if filter_date != '' and filter_date is not None:
            objects = objects.filter(
                Q(agent_float_requested_at__gte=filter_date))
            objects = objects.filter(
                Q(agent_float_requested_at__lt=filter_date+86400))
        if filter_agent != '' and filter_agent != '-1':
            objects = objects.filter(
                Q(agent_float_requested_by=filter_agent))
        if filter_company != '' and filter_company != '-1':
            objects = objects.filter(
                Q(agent_float_company_id=filter_company))
        
        if balance:
            agent_float_old_balance = 0
            agent_float_new_balance = 0
            if filter_status == Agent_Floats_Tickets.STATUS_APPROVED:
                objects_first = objects_last = objects
                first = objects_first.all().first()
                if first is not None:
                    agent_float_old_balance = first.agent_float_old_balance
                last = objects_last.all().last()
                if last is not None:
                    agent_float_new_balance = last.agent_float_new_balance
            return agent_float_old_balance, agent_float_new_balance

        amount = int(objects.all().aggregate(
            Sum('agent_float_amount'))['agent_float_amount__sum'] or 0)
        count = objects.count()
        return amount, count
