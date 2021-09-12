from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from backend.views import card_log_views

urlpatterns = [

    # card_logs
    path('', card_log_views.index, name='index'),
    url(r'^card-logs/datatable/$',
        card_log_views.AjaxCardLogsList.as_view(), name='card_logs_datatable'),

    # index
    url(r'^card-logs/datatable/$',
        card_log_views.AjaxCardLogsList.as_view(), name='card_logs_datatable'),
    url(r'^card-logs/index/$', card_log_views.index,
        name='card_logs_index'),
    url(r'^card-logs/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # view
    url(r'^card_logs/view/(?P<pk>.+)/$',
        card_log_views.view, name='card_logs_view'),
    url(r'^card_logs/view/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
