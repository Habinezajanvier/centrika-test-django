from django.urls import re_path, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import tickets_external_views

urlpatterns = [

    # tickets_external
    path('', tickets_external_views.index, name='index'),
    re_path(r'^tickets-external/datatable/$',
        tickets_external_views.AjaxTicketsExternalList.as_view(), name='tickets_external_datatable'),

    # index
    re_path(r'^tickets-external/index/$', tickets_external_views.index,
        name='tickets_external_index'),
    re_path(r'^tickets-external/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # view
    re_path(r'^tickets_external/view/(?P<pk>.+)/$',
        tickets_external_views.view, name='tickets_external_view'),
    re_path(r'^tickets_external/view/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
