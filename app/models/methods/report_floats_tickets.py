

from django.conf import settings
from app.models.agent_floats_tickets import Agent_Floats_Tickets
from django.db.models.aggregates import Sum
from django.db.models import Q


class Report_Floats_Tickets():
    @staticmethod
    def get_data_by_values(request, operator, filter_start_time, filter_end_time, filter_action, filter_status, filter_agent):
        if filter_start_time != '' and filter_start_time is not None:
            filter_start_time = int(filter_start_time.strftime(
                '%s')) + settings.TIME_DIFFERENCE
        if filter_end_time != '' and filter_end_time is not None:
            filter_end_time = int(filter_end_time.strftime(
                '%s')) + settings.TIME_DIFFERENCE
        # filtered
        # transactions frw
        objects = Agent_Floats_Tickets.objects
        objects = objects.filter(
            Q(agent_float_status=filter_status))
        if filter_status == Agent_Floats_Tickets.STATUS_PENDING:
            if filter_start_time != '' and filter_start_time is not None:
                objects = objects.filter(
                    Q(agent_float_requested_at__gte=filter_start_time))
            if filter_end_time != '' and filter_end_time is not None:
                objects = objects.filter(
                    Q(agent_float_requested_at__lte=filter_end_time))
        else:
            if filter_start_time != '' and filter_start_time is not None:
                objects = objects.filter(
                    Q(agent_float_approval_updated_at__gte=filter_start_time))
            if filter_end_time != '' and filter_end_time is not None:
                objects = objects.filter(
                    Q(agent_float_approval_updated_at__lte=filter_end_time))
        if filter_agent != '' and filter_agent != '-1':
            objects = objects.filter(
                Q(agent_float_requested_by=filter_agent))
        transactions_amount_filter = int(objects.all().aggregate(
            Sum('agent_float_amount'))['agent_float_amount__sum'] or 0)
        transactions_count_filter = objects.count()
        return transactions_amount_filter, transactions_count_filter

    @staticmethod
    def get_data(request, operator, filter_form):
        filter_start_time = filter_form.cleaned_data['start_time']
        if filter_start_time != '' and filter_start_time is not None:
            filter_start_time = int(filter_start_time.strftime(
                '%s')) + settings.TIME_DIFFERENCE
        filter_end_time = filter_form.cleaned_data['end_time']
        if filter_end_time != '' and filter_end_time is not None:
            filter_end_time = int(filter_end_time.strftime(
                '%s')) + settings.TIME_DIFFERENCE
        filter_action = filter_form.cleaned_data['action']
        filter_status = filter_form.cleaned_data['status']
        filter_agent = filter_form.cleaned_data['agent']
        # filtered
        # transactions frw
        objects = Agent_Floats_Tickets.objects
        objects = objects.filter(
            Q(agent_float_status=filter_status))
        if filter_status == Agent_Floats_Tickets.STATUS_PENDING:
            if filter_start_time != '' and filter_start_time is not None:
                objects = objects.filter(
                    Q(agent_float_requested_at__gte=filter_start_time))
            if filter_end_time != '' and filter_end_time is not None:
                objects = objects.filter(
                    Q(agent_float_requested_at__lte=filter_end_time))
        else:
            if filter_start_time != '' and filter_start_time is not None:
                objects = objects.filter(
                    Q(agent_float_approval_updated_at__gte=filter_start_time))
            if filter_end_time != '' and filter_end_time is not None:
                objects = objects.filter(
                    Q(agent_float_approval_updated_at__lte=filter_end_time))
        if filter_agent != '' and filter_agent != '-1':
            objects = objects.filter(
                Q(agent_float_requested_by=filter_agent))
        transactions_amount_filter = int(objects.all().aggregate(
            Sum('agent_float_amount'))['agent_float_amount__sum'] or 0)
        transactions_count_filter = objects.count()
        return transactions_amount_filter, transactions_count_filter
