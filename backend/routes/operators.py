from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from backend.views import operator_views

urlpatterns = [

    # operators
    path('', operator_views.index, name='index'),
    url(r'^operators/datatable/$',
        operator_views.AjaxOperatorsList.as_view(), name='operators_datatable'),

    # signup and confirmation
    url(r'^operators/signup/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
    url(r'^operators/signup/confirm/(?P<token>.+)/$',
        operator_views.confirm, name='operators_signup_confirm'),

    # signin
    url(r'^operators/signin/$', operator_views.signin, name='operators_signin'),
    url(r'^operators/signin/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # forgot password
    url(r'^operators/forgot-password/$', operator_views.forgot_password,
        name='operators_forgot_password'),
    url(r'^operators/forgot-password/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # reset password
    url(r'^operators/reset-password/(?P<token>.+)',
        operator_views.reset_password, name='operators_reset_password'),
    # url(r'^operators/reset-password/(?P<token>.+)/service-worker.js',
    #     (TemplateView.as_view(template_name="service-worker/service-worker.js",
    #                           content_type='application/javascript', )),
    #     name='service-worker.js'),

    # signout
    url(r'^operators/signout/$', operator_views.signout, name='operators_signout'),

    # dashboard
    url(r'^operators/dashboard/$', operator_views.dashboard,
        name='operators_dashboard'),
    url(r'^operators/dashboard/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # index
    url(r'^operators/json/$', operator_views.json_operators, name='json_operators'),
    url(r'^operators/index/$', operator_views.index, name='operators_index'),
    url(r'^operators/index/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # single or multiple select
    url(r'^operators/select-single/$', operator_views.select_single,
        name='operators_select_single'),
    url(r'^operators/select-multiple/$', operator_views.select_multiple,
        name='operators_select_multiple'),

    # create
    url(r'^operators/create/$', operator_views.create, name='operators_create'),
    url(r'^operators/create/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update
    url(r'^operators/update/(?P<pk>.+)/$',
        operator_views.update, name='operators_update'),
    url(r'^operators/update/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),

    # update permissions
    url(r'^operators/update-permissions/(?P<pk>.+)/$', operator_views.update_permissions_view,
        name='operators_update_permissions_view'),
    url(r'^operators/update-permissions/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
    url(r'^operators/update-permissions/$', operator_views.update_permissions_action,
        name='operators_update_permissions_action'),

    # view
    url(r'^operators/view/(?P<pk>.+)/$',
        operator_views.view, name='operators_view'),
    url(r'^operators/view/(?P<pk>.+)/service-worker.js',
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

    # update-reset-password
    url(r'^operators/update-reset-password/(?P<pk>.+)/$', operator_views.update_reset_password,
        name='operators_update_reset_password'),
    url(r'^operators/update-reset-password/(?P<pk>.+)/service-worker.js',
        (TemplateView.as_view(template_name="service-worker/service-worker.js",
                              content_type='application/javascript', )),
        name='service-worker.js'),
]
