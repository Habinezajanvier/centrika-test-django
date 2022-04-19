from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from backend.views import operator_views

urlpatterns = [

    # signin
    url(r'^operators/signin/$', operator_views.signin, name='operators_signin'),
    url(r'^operators/signin/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # signout
    url(r'^operators/signout/$', operator_views.signout, name='operators_signout'),

    # dashboard
    url(r'^operators/dashboard/$', operator_views.dashboard,
        name='operators_dashboard'),
    url(r'^operators/dashboard/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-view
    url(r'^operators/profile/view/$', operator_views.profile_view,
        name='operators_profile_view'),
    url(r'^operators/profile/view/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-update
    url(r'^operators/profile/update/$', operator_views.profile_update,
        name='operators_profile_update'),
    url(r'^operators/profile/update/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-change-password
    url(r'^operators/profile/change-password/$', operator_views.profile_change_password,
        name='operators_profile_change_password'),
    url(r'^operators/profile/change-password/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
