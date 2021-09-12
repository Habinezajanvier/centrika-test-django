from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from app import settings
from app.models.methods.operators import Methods_Operators
from app.models.operators import Operators
from app.models.organizations import Organizations
from django.urls import reverse
from django.utils.safestring import mark_safe


class OperatorsTable(tables.Table):
    auth_permissions = {}

    row_number = tables.Column(
        verbose_name='Id',
        attrs={
            'search_filter': '',
            'th_style': 'width:60px;',
        },
        orderable=False,
        empty_values=(),
        accessor='pk',
    )
    operator_username = tables.Column(
        verbose_name='Email Id',
        attrs={
            'search_filter': 'input-text',
        }
    )
    operator_name = tables.Column(
        verbose_name='Name',
        attrs={
            'search_filter': 'input-text',
        }
    )
    operator_contact_phone_number = tables.Column(
        verbose_name='Phone Number',
        attrs={
            'search_filter': 'input-text',
        }
    )
    operator_organization_id = tables.Column(
        verbose_name='Organization',
        attrs={
            'search_filter': 'input-text',
        }
    )
    operator_status = tables.Column(
        verbose_name='Status',
        attrs={
            'search_filter': 'input-select',
            'search_data': Operators.ARRAY_TEXT_STATUS,
            'search_type': 'status',
            'th_style': 'width:100px;',
        }
    )
    actions = tables.Column(
        verbose_name='Actions',
        attrs={
            'search_filter': '',
            'th_style': 'width:81px;',
        },
        orderable=False,
        empty_values=(),
    )

    def __init__(self, *args, **kwargs):
        self.counter = itertools.count(1)
        super(OperatorsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = '<a href=' + str(record.pk) + '>' + '%d' % counter + '</a>'
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        # action_data = ""
        data = ''
        if settings.ACCESS_PERMISSION_OPERATOR_VIEW in auth_permissions.values():
            url = reverse("operators_view", args=[record.pk])
            data += '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \'' + \
                url+'\';"><i class="fa fa-eye"></i></button>&nbsp;'
            # action_data = action_data + \
            #     "<a class=\"btn btn-default btn-block\" href=\"" + url + "\">View</a>"
        if settings.ACCESS_PERMISSION_OPERATOR_UPDATE in auth_permissions.values():
            url = reverse("operators_update", args=[record.pk])
            data += '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \'' + \
                url+'\';"><i class="fa fa-edit"></i></button>&nbsp;'
            # action_data = action_data + \
            #     "<a class=\"btn btn-default btn-block\" href=\"" + url + "\">Update</a>"
        # if settings.ACCESS_PERMISSION_OPERATOR_UPDATE in auth_permissions.values() and record.operator_status == Operators.STATUS_UNVERIFIED:
        #     url = reverse("operators_select_single")
        #     action_data = action_data + "<a class=\"btn btn-default btn-block\" href=\"#\" onclick=\"javascript: singleSelect(\'" + url + "\', \'verify\', \'" + str(
        #         record.operator_id) + "\');\">Verify</a>"
        # if settings.ACCESS_PERMISSION_OPERATOR_UPDATE in auth_permissions.values() and record.operator_status == Operators.STATUS_UNAPPROVED:
        #     url = reverse("operators_select_single")
        #     action_data = action_data + "<a class=\"btn btn-default btn-block\" href=\"#\" onclick=\"javascript: singleSelect(\'" + url + "\', \'approve\', \'" + str(
        #         record.operator_id) + "\');\">Approve</a>"
        # if settings.ACCESS_PERMISSION_OPERATOR_UPDATE in auth_permissions.values() and (
        #         record.operator_status == Operators.STATUS_ACTIVE or record.operator_status == Operators.STATUS_INACTIVE):
        #     url = reverse("operators_select_single")
        #     action_data = action_data + "<a class=\"btn btn-default btn-block\" href=\"#\" onclick=\"javascript: singleSelect(\'" + url + "\', \'block\', \'" + str(
        #         record.operator_id) + "\');\">Block</a>"
        # if settings.ACCESS_PERMISSION_OPERATOR_UPDATE in auth_permissions.values() and record.operator_status == Operators.STATUS_BLOCKED:
        #     url = reverse("operators_select_single")
        #     action_data = action_data + "<a class=\"btn btn-default btn-block\" href=\"#\" onclick=\"javascript: singleSelect(\'" + url + "\', \'unblock\', \'" + str(
        #         record.operator_id) + "\');\">Unblock</a>"
        if settings.ACCESS_PERMISSION_OPERATOR_DELETE in auth_permissions.values():
            url = reverse("operators_select_single")
            data += '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\'' + url + '\', \'delete\', \'' + str(
                record.operator_id) + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'
            # action_data = action_data + "<a class=\"btn btn-default btn-block\" href=\"#\" onclick=\"javascript: singleSelect(\'" + url + "\', \'delete\', \'" + str(
            #     record.operator_id) + "\');\">Delete</a>"

        # data = '<div class="dt-buttons">' \
        #        '<div class="btn-group">' \
        #        '<button class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false"> Action &nbsp;&nbsp;<i class="fa fa-caret-down"></i></button>' \
        #        '<ul class="dropdown-menu action-menu">' \
        #        '<div class="dt-button-collection">' \
        #        + action_data + \
        #        '</div>' \
        #        '</ul>' \
        #        '</div>' \
        #        '</div>'

        return data

    @staticmethod
    def render_operator_username(record):
        return mark_safe(
            '<a href=' + reverse("operators_view",
                                 args=[record.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
            str(record.operator_username) + '</a>')

    @staticmethod
    def render_operator_name(record):
        return record.operator_name

    @staticmethod
    def render_operator_contact_phone_number(record):
        return record.operator_contact_phone_number

    @staticmethod
    def render_operator_organization_id(record, auth_permissions):
        if record.operator_organization_id == 0:
            return 'All'
        try:
            organization = Organizations.objects.get(
                pk=record.operator_organization_id)
            if settings.ACCESS_PERMISSION_ORGANIZATION_VIEW in auth_permissions.values():
                return mark_safe(
                    '<a href=' + reverse("organizations_view",
                                         args=[organization.organization_id]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
                    str(organization.organization_name) + '</a>')
            else:
                return str(organization.organization_name)
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            return record.operator_organization_id

    @staticmethod
    def render_operator_status(record):
        if record.operator_status == Operators.STATUS_ACTIVE:
            value = Operators.HTML_TAG_STATUS_ACTIVE_COLOR
        elif record.operator_status == Operators.STATUS_BLOCKED:
            value = Operators.HTML_TAG_STATUS_BLOCKED_COLOR
        elif record.operator_status == Operators.STATUS_UNVERIFIED:
            value = Operators.HTML_TAG_STATUS_UNVERIFIED_COLOR
        elif record.operator_status == Operators.STATUS_UNAPPROVED:
            value = Operators.HTML_TAG_STATUS_UNAPPROVED_COLOR
        else:
            value = Operators.HTML_TAG_STATUS_INACTIVE_COLOR
        return value

    class Meta:
        model = Operators
        order_column_index = 1
        order_column_sort = 'asc'
        attrs = {
            'id': 'table-' + Operators.NAME,
            'name': Operators.NAME,
            'class': 'table table-bordered table-hover thead-dark table-responsive',
            'cellspacing': '0',
            'width': '100%',
            'default_order': [order_column_index, order_column_sort],
            'table_columns': [
                {
                    "data": "row_number",
                },
                {
                    "data": "operator_username",
                },
                {
                    "data": "operator_name",
                },
                {
                    "data": "operator_contact_phone_number",
                },
                {
                    "data": "operator_organization_id",
                },
                {
                    "data": "operator_status",
                },
                {
                    "data": "actions",
                },
            ],

        }
        sequence = (
            'row_number',
            'operator_username',
            'operator_name',
            'operator_contact_phone_number',
            'operator_organization_id',
            'operator_status',
            'actions'
        )
        fields = (
            'operator_username',
            'operator_name',
            'operator_contact_phone_number',
            'operator_organization_id',
            'operator_status',
        )
        template_name = '_include/bootstrap-datatable-server.html'
