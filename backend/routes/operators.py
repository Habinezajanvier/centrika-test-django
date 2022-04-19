from django.urls import re_path, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import operator_views

urlpatterns = [

    # signin
    re_path(r'^operators/signin/$', operator_views.signin, name='operators_signin'),
    re_path(r'^operators/signin/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # signout
    re_path(r'^operators/signout/$', operator_views.signout, name='operators_signout'),

    # dashboard
    re_path(r'^operators/dashboard/$', operator_views.dashboard,
        name='operators_dashboard'),
    re_path(r'^operators/dashboard/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-view
    re_path(r'^operators/profile/view/$', operator_views.profile_view,
        name='operators_profile_view'),
    re_path(r'^operators/profile/view/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-update
    re_path(r'^operators/profile/update/$', operator_views.profile_update,
        name='operators_profile_update'),
    re_path(r'^operators/profile/update/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # profile-change-password
    re_path(r'^operators/profile/change-password/$', operator_views.profile_change_password,
        name='operators_profile_change_password'),
    re_path(r'^operators/profile/change-password/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
