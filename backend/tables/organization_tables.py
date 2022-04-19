from __future__ import unicode_literals

import itertools

import django_tables2 as tables
from app import settings
from app.models.methods.organizations import Methods_Organizations
from app.models.organizations import Organizations
from django.urls import reverse
from django.utils.safestring import mark_safe


class OrganizationsTable(tables.Table):
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
    organization_name = tables.Column(
        verbose_name='Name',
        attrs={
            'search_filter': 'input-text',
        }
    )
    organization_email_id = tables.Column(
        verbose_name='Email Id',
        attrs={
            'search_filter': 'input-text',
        }
    )
    organization_phone_number = tables.Column(
        verbose_name='Phone Number',
        attrs={
            'search_filter': 'input-text',
        }
    )
    organization_status = tables.Column(
        verbose_name='Status',
        attrs={
            'search_filter': 'input-select',
            'search_data': Organizations.ARRAY_TEXT_STATUS,
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
        super(OrganizationsTable, self).__init__(*args, **kwargs)

    def set_auth_permissions(self, auth_permissions):
        self.auth_permissions = auth_permissions

    @staticmethod
    def render_row_number(record, counter):
        value = '<a href=' + str(record.pk) + '>' + '%d' % counter + '</a>'
        return value

    @staticmethod
    def render_actions(record, auth_permissions):
        data = ''
        if settings.ACCESS_PERMISSION_ORGANIZATION_VIEW in auth_permissions.values():
            url = reverse("organizations_view", args=[record.pk])
            data += '<button class="demo-delete-row btn btn-info btn-xs" onclick="javascript:location.href = \'' + \
                url+'\';"><i class="fa fa-eye"></i></button>&nbsp;'
        if settings.ACCESS_PERMISSION_ORGANIZATION_UPDATE in auth_permissions.values():
            url = reverse("organizations_update", args=[record.pk])
            data += '<button class="demo-delete-row btn btn-warning btn-xs" onclick="javascript:location.href = \'' + \
                url+'\';"><i class="fa fa-edit"></i></button>&nbsp;'
        if settings.ACCESS_PERMISSION_ORGANIZATION_DELETE in auth_permissions.values():
            url = reverse("organizations_select_single")
            data += '<button class = "demo-delete-row btn btn-danger btn-xs" onclick="javascript: singleSelect(\'' + url + '\', \'delete\', \'' + str(
                record.organization_id) + '\');" ><i class="fa fa-trash"></i></button>&nbsp;'

        return data

    @staticmethod
    def render_organization_name(record):
        return mark_safe(
            '<a href=' + reverse("organizations_view",
                                 args=[record.pk]) + ' style=\'text-decoration:underline; color:#1B82DC;\' >' +
            str(record.organization_name) + '</a>')

    @staticmethod
    def render_organization_email_id(record):
        return record.organization_email_id

    @staticmethod
    def render_organization_phone_number(record):
        return record.organization_phone_number

    @staticmethod
    def render_organization_status(record):
        if record.organization_status == Organizations.STATUS_ACTIVE:
            value = Organizations.HTML_TAG_STATUS_ACTIVE_COLOR
        elif record.organization_status == Organizations.STATUS_BLOCKED:
            value = Organizations.HTML_TAG_STATUS_BLOCKED_COLOR
        return value

    class Meta:
        model = Organizations
        order_column_index = 1
        order_column_sort = 'asc'
        attrs = {
            'id': 'table-' + Organizations.NAME,
            'name': Organizations.NAME,
            'class': 'table table-bordered table-hover thead-dark table-responsive',
            'cellspacing': '0',
            'width': '100%',
            'default_order': [order_column_index, order_column_sort],
            'table_columns': [
                {
                    "data": "row_number",
                },
                {
                    "data": "organization_name",
                },
                {
                    "data": "organization_email_id",
                },
                {
                    "data": "organization_phone_number",
                },
                {
                    "data": "organization_status",
                },
                {
                    "data": "actions",
                },
            ],

        }
        sequence = (
            'row_number',
            'organization_name',
            'organization_email_id',
            'organization_phone_number',
            'organization_status',
            'actions'
        )
        fields = (
            'organization_name',
            'organization_email_id',
            'organization_phone_number',
            'organization_status',
        )
        template_name = '_include/bootstrap-datatable-server.html'