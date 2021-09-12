from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from backend.views import organization_views

urlpatterns = [

    # organizations
    path('', organization_views.index, name='index'),
    url(r'^organizations/datatable/$',
        organization_views.AjaxOrganizationsList.as_view(), name='organizations_datatable'),

    # index
    url(r'^organizations/json/$', organization_views.json_organizations, name='json_organizations'),
    url(r'^organizations/index/$', organization_views.index, name='organizations_index'),
    url(r'^organizations/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # single or multiple select
    url(r'^organizations/select-single/$', organization_views.select_single,
        name='organizations_select_single'),
    url(r'^organizations/select-multiple/$', organization_views.select_multiple,
        name='organizations_select_multiple'),

    # create
    url(r'^organizations/create/$', organization_views.create, name='organizations_create'),
    url(r'^organizations/create/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update
    url(r'^organizations/update/(?P<pk>.+)/$',
        organization_views.update, name='organizations_update'),
    url(r'^organizations/update/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # view
    url(r'^organizations/view/(?P<pk>.+)/$',
        organization_views.view, name='organizations_view'),
    url(r'^organizations/view/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
