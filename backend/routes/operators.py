from django.urls import re_path, include
from django.urls import path
from django.views.generic import TemplateView

from backend.views import operator_views

urlpatterns = [

    # operators
    path('', operator_views.index, name='index'),
    re_path(r'^operators/datatable/$',
        operator_views.AjaxOperatorsList.as_view(), name='operators_datatable'),

    # signup and confirmation
    re_path(r'^operators/signup/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
    re_path(r'^operators/signup/confirm/(?P<token>.+)/$',
        operator_views.confirm, name='operators_signup_confirm'),

    # signin
    re_path(r'^operators/signin/$', operator_views.signin, name='operators_signin'),
    re_path(r'^operators/signin/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # forgot password
    re_path(r'^operators/forgot-password/$', operator_views.forgot_password,
        name='operators_forgot_password'),
    re_path(r'^operators/forgot-password/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # reset password
    re_path(r'^operators/reset-password/(?P<token>.+)',
        operator_views.reset_password, name='operators_reset_password'),
    # re_path(r'^operators/reset-password/(?P<token>.+)/service-worker.js',
    #     (TemplateView.as_view(template_name="service-worker/service-worker.js",
    #                           content_type='application/javascript', )),
    #     name='service-worker.js'),

    # signout
    re_path(r'^operators/signout/$', operator_views.signout, name='operators_signout'),

    # dashboard
    re_path(r'^operators/dashboard/$', operator_views.dashboard,
        name='operators_dashboard'),
    re_path(r'^operators/dashboard/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # index
    re_path(r'^operators/json/$', operator_views.json_operators, name='json_operators'),
    re_path(r'^operators/index/$', operator_views.index, name='operators_index'),
    re_path(r'^operators/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # single or multiple select
    re_path(r'^operators/select-single/$', operator_views.select_single,
        name='operators_select_single'),
    re_path(r'^operators/select-multiple/$', operator_views.select_multiple,
        name='operators_select_multiple'),

    # create
    re_path(r'^operators/create/$', operator_views.create, name='operators_create'),
    re_path(r'^operators/create/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update
    re_path(r'^operators/update/(?P<pk>.+)/$',
        operator_views.update, name='operators_update'),
    re_path(r'^operators/update/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update permissions
    re_path(r'^operators/update-permissions/(?P<pk>.+)/$', operator_views.update_permissions_view,
        name='operators_update_permissions_view'),
    re_path(r'^operators/update-permissions/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
    re_path(r'^operators/update-permissions/$', operator_views.update_permissions_action,
        name='operators_update_permissions_action'),

    # view
    re_path(r'^operators/view/(?P<pk>.+)/$',
        operator_views.view, name='operators_view'),
    re_path(r'^operators/view/(?P<pk>.+)/service-worker.js',
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

    # update-reset-password
    re_path(r'^operators/update-reset-password/(?P<pk>.+)/$', operator_views.update_reset_password,
        name='operators_update_reset_password'),
    re_path(r'^operators/update-reset-password/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]