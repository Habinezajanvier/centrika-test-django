from django.urls import re_path, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import card_log_views

urlpatterns = [

    # card_logs
    path('', card_log_views.index, name='index'),
    re_path(r'^card-logs/datatable/$',
        card_log_views.AjaxCardLogsList.as_view(), name='card_logs_datatable'),

    # index
    re_path(r'^card-logs/index/$', card_log_views.index,
        name='card_logs_index'),
    re_path(r'^card-logs/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # view
    re_path(r'^card_logs/view/(?P<pk>.+)/$',
        card_log_views.view, name='card_logs_view'),
    re_path(r'^card_logs/view/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
