from django.urls import re_path, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import organization_views

urlpatterns = [

    # organizations
    path('', organization_views.index, name='index'),
    re_path(r'^organizations/datatable/$',
        organization_views.AjaxOrganizationsList.as_view(), name='organizations_datatable'),

    # index
    re_path(r'^organizations/json/$', organization_views.json_organizations, name='json_organizations'),
    re_path(r'^organizations/index/$', organization_views.index, name='organizations_index'),
    re_path(r'^organizations/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # single or multiple select
    re_path(r'^organizations/select-single/$', organization_views.select_single,
        name='organizations_select_single'),
    re_path(r'^organizations/select-multiple/$', organization_views.select_multiple,
        name='organizations_select_multiple'),

    # create
    re_path(r'^organizations/create/$', organization_views.create, name='organizations_create'),
    re_path(r'^organizations/create/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update
    re_path(r'^organizations/update/(?P<pk>.+)/$',
        organization_views.update, name='organizations_update'),
    re_path(r'^organizations/update/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # view
    re_path(r'^organizations/view/(?P<pk>.+)/$',
        organization_views.view, name='organizations_view'),
    re_path(r'^organizations/view/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]