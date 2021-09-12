from api.v1 import api_views
from django.conf.urls import url

urlpatterns = [
    url(r'^api/v1/operators/login/$',
        api_views.operator_login, name='v1_api_views_operator_login'),
    url(r'^api/v1/card-topup/$',
        api_views.card_topup, name='v1_api_views_card_topup'),
    url(r'^api/v1/card-topup-complete/$',
        api_views.card_topup_complete, name='v1_api_views_card_topup_complete'),
    url(r'^api/v1/card-balance/$',
        api_views.card_balance, name='v1_api_views_card_balance'),
    url(r'^api/v1/card-balance-complete/$',
        api_views.card_balance_complete, name='v1_api_views_card_balance_complete'),
]
