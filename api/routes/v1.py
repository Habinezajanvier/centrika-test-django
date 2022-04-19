from api.v1 import api_views
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^api/v1/operators/login/$',
        api_views.operator_login, name='v1_api_views_operator_login'),
    re_path(r'^api/v1/card-balance/$',
        api_views.card_balance, name='v1_api_views_card_balance'),
    re_path(r'^api/v1/card-balance-complete/$',
        api_views.card_balance_complete, name='v1_api_views_card_balance_complete'),
    re_path(r'^api/v1/card-topup/$',
        api_views.card_topup, name='v1_api_views_card_topup'),
    re_path(r'^api/v1/card-topup-complete/$',
        api_views.card_topup_complete, name='v1_api_views_card_topup_complete'),
    re_path(r'^api/v1/card-pay/$',
        api_views.card_pay, name='v1_api_views_card_pay'),
    re_path(r'^api/v1/card-pay-complete/$',
        api_views.card_pay_complete, name='v1_api_views_card_pay_complete'),
]
