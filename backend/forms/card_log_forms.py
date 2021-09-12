from django import forms
from prettyjson import PrettyJSONWidget

from app.models.card_logs import Card_Logs
from backend import admin


class JsonForm(forms.ModelForm):
    class Meta:
        model = Card_Logs
        fields = '__all__'
        widgets = {
            'card_log_login_request_body': PrettyJSONWidget(),
            'card_log_login_response': PrettyJSONWidget(),
            'card_log_start_session_request_body': PrettyJSONWidget(),
            'card_log_start_session_response': PrettyJSONWidget(),
            'card_log_get_purse_1_request_body': PrettyJSONWidget(),
            'card_log_get_purse_1_response': PrettyJSONWidget(),
            'card_log_web_top_up_request_body': PrettyJSONWidget(),
            'card_log_web_top_up_response': PrettyJSONWidget(),
            'card_log_get_purse_2_request_body': PrettyJSONWidget(),
            'card_log_get_purse_2_response': PrettyJSONWidget(),
            'card_log_end_session_request_body': PrettyJSONWidget(),
            'card_log_end_session_response': PrettyJSONWidget(),
        }


class JsonAdmin(admin.ModelAdmin):
  form = JsonForm
