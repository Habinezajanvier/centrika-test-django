# Generated by Django 4.0.2 on 2022-04-19 15:22

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access_Permissions',
            fields=[
                ('access_permission_name', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='Access Permission Name')),
                ('access_permission_details', models.CharField(blank=True, max_length=255, verbose_name='Details')),
                ('access_permission_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
            ],
            options={
                'db_table': 'access_permissions',
            },
        ),
        migrations.CreateModel(
            name='Card_Balance',
            fields=[
                ('card_balance_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Card Balance Id')),
                ('card_balance_card_id', models.IntegerField(default=0, verbose_name='Card')),
                ('card_balance_company_id', models.IntegerField(default=0, verbose_name='Company')),
                ('card_balance_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='Amount')),
                ('card_balance_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('card_balance_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('card_balance_status', models.IntegerField(default=1, verbose_name='Status')),
            ],
            options={
                'db_table': 'card_balance',
            },
        ),
        migrations.CreateModel(
            name='Card_Logs',
            fields=[
                ('card_log_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Card Log Id')),
                ('card_log_card_number', models.CharField(max_length=255, verbose_name='Card Number')),
                ('card_log_device_serial_number', models.CharField(max_length=255, verbose_name='Device Serial No.')),
                ('card_log_institution_code', models.CharField(max_length=255, verbose_name='Institution Code')),
                ('card_log_network_id', models.CharField(max_length=255, verbose_name='Network Id')),
                ('card_log_login_request_body', models.TextField(blank=True, verbose_name='Start Session Request Body')),
                ('card_log_login_response', models.TextField(blank=True, verbose_name='Start Session Response')),
                ('card_log_start_session_request_body', models.TextField(blank=True, verbose_name='Start Session Request Body')),
                ('card_log_start_session_response', models.TextField(blank=True, verbose_name='Start Session Response')),
                ('card_log_get_purse_1_request_body', models.TextField(blank=True, verbose_name='Get Purse Request Body')),
                ('card_log_get_purse_1_response', models.TextField(blank=True, verbose_name='Get Purse Response')),
                ('card_log_web_top_up_request_body', models.TextField(blank=True, verbose_name='Web Top Up Request Body')),
                ('card_log_web_top_up_response', models.TextField(blank=True, verbose_name='Web Top Up Response')),
                ('card_log_get_purse_2_request_body', models.TextField(blank=True, verbose_name='Get Purse Request Body')),
                ('card_log_get_purse_2_response', models.TextField(blank=True, verbose_name='Get Purse Response')),
                ('card_log_end_session_request_body', models.TextField(blank=True, verbose_name='End Session Request Body')),
                ('card_log_end_session_response', models.TextField(blank=True, verbose_name='End Session Response')),
                ('card_log_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='Amount')),
                ('card_log_old_balance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='Old Balance')),
                ('card_log_new_balance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='New Balance')),
                ('card_log_response', models.TextField(blank=True, verbose_name='Response')),
                ('card_log_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('card_log_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('card_log_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('card_log_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
            options={
                'db_table': 'asis_card_logs',
            },
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Card Id')),
                ('card_type', models.IntegerField(default=0, verbose_name='Type')),
                ('card_number', models.CharField(max_length=100, unique=True, verbose_name='Number')),
                ('card_customer_id', models.IntegerField(default=0, verbose_name='Customer')),
                ('card_balance', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='Balance')),
                ('card_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('card_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('card_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('card_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('card_status', models.IntegerField(default=1, verbose_name='Status')),
            ],
            options={
                'db_table': 'cards',
            },
        ),
        migrations.CreateModel(
            name='Failed_Login',
            fields=[
                ('failed_login_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('failed_login_username', models.CharField(max_length=255, verbose_name='Username')),
                ('failed_login_password', models.CharField(max_length=255, verbose_name='Password')),
                ('failed_login_from', models.CharField(choices=[('backend', 'backend'), ('frontend', 'frontend')], default='frontend', max_length=10, verbose_name='From')),
                ('failed_login_ip_address', models.CharField(max_length=100, verbose_name='Ip Address')),
                ('failed_login_attempted_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('failed_login_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
            options={
                'db_table': 'failed_login',
            },
        ),
        migrations.CreateModel(
            name='Operator_Access_Permissions',
            fields=[
                ('operator_access_permission_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('operator_access_permission_name', models.CharField(default='', max_length=255, verbose_name='Name')),
                ('operator_access_permission_operator_id', models.IntegerField(default=0, verbose_name='Operator')),
                ('operator_access_permission_created_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('operator_access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated By')),
            ],
            options={
                'db_table': 'operator_access_permissions',
            },
        ),
        migrations.CreateModel(
            name='Operators',
            fields=[
                ('operator_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Operator Id')),
                ('operator_username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('operator_auth_key', models.CharField(max_length=255, verbose_name='Auth key')),
                ('operator_password', models.CharField(max_length=255, verbose_name='Password')),
                ('operator_password_reset_token', models.CharField(blank=True, max_length=255, verbose_name='Password reset token')),
                ('operator_type', models.IntegerField(default=0, verbose_name='type')),
                ('operator_company_id', models.IntegerField(default=0, verbose_name='Company')),
                ('operator_first_name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('operator_last_name', models.CharField(blank=True, max_length=100, verbose_name='Last Name')),
                ('operator_gender', models.IntegerField(default=0, verbose_name='Gender')),
                ('operator_email_id', models.EmailField(blank=True, max_length=100, verbose_name='Email id')),
                ('operator_phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+250123456789'. Up to 13 digits allowed.", regex='^\\+?1?\\d{9,15}$'), django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(13)], verbose_name='Phone Number')),
                ('operator_address', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('operator_profile_photo', models.CharField(blank=True, max_length=255, verbose_name='Profile photo file path')),
                ('operator_signature', models.CharField(blank=True, max_length=255, verbose_name='Signature')),
                ('operator_buses', models.CharField(blank=True, max_length=255, verbose_name='Operator Buses')),
                ('operator_organization', models.CharField(default='0', max_length=255, verbose_name='Organization')),
                ('operator_ip_address', models.CharField(blank=True, max_length=100, verbose_name='IP Address')),
                ('operator_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('operator_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('operator_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('operator_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('operator_status', models.IntegerField(default=0, verbose_name='Status')),
            ],
            options={
                'db_table': 'operators',
            },
        ),
        migrations.CreateModel(
            name='Tickets_External',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Ticket Id')),
                ('ticket_external', models.CharField(default='', max_length=255, verbose_name='Organization')),
                ('ticket_reference', models.CharField(default='', max_length=255, verbose_name='Reference Ticket Id')),
                ('ticket_company_name', models.CharField(default='', max_length=255, verbose_name='Company')),
                ('ticket_company_branch_name', models.CharField(default='', max_length=255, verbose_name='Branch')),
                ('ticket_agent_name', models.CharField(default='', max_length=255, verbose_name='Agent')),
                ('ticket_route_name', models.CharField(default='', max_length=255, verbose_name='Bus Route')),
                ('ticket_bus_plate_number', models.CharField(default='', max_length=255, verbose_name='Bus Plate Number')),
                ('ticket_destination_name', models.CharField(default='', max_length=255, verbose_name='Destination')),
                ('ticket_schedule_id', models.CharField(default='', max_length=255, verbose_name='Trip Id')),
                ('ticket_start_bus_stop_name', models.CharField(default='', max_length=255, verbose_name='Start Stop')),
                ('ticket_end_bus_stop_name', models.CharField(default='', max_length=255, verbose_name='End Stop')),
                ('ticket_customer_name', models.CharField(default='', max_length=255, verbose_name='Customer Name')),
                ('ticket_customer_phone_number', models.CharField(default='', max_length=255, verbose_name='Customer Phone')),
                ('ticket_pos_serial_number', models.CharField(default='', max_length=255, verbose_name='Pos')),
                ('ticket_travel_date', models.DateField(blank=True, null=True, verbose_name='Travel Date')),
                ('ticket_travel_time', models.TimeField(blank=True, null=True, verbose_name='Travel Time')),
                ('ticket_travel_datetime', models.DateTimeField(default='', max_length=255, verbose_name='Travel Datetime')),
                ('ticket_price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=30, verbose_name='Ticeket Price')),
                ('ticket_payment_type', models.CharField(default='', max_length=255, verbose_name='Payment Type')),
                ('ticket_payment_provider', models.CharField(default='', max_length=255, verbose_name='Payment Provider')),
                ('ticket_card_number', models.CharField(default='', max_length=255, verbose_name='Card Number')),
                ('ticket_card_response', models.CharField(default='', max_length=255, verbose_name='Card Response')),
                ('ticket_card_transaction_id', models.CharField(default='', max_length=255, verbose_name='Card Transaction Id')),
                ('ticket_card_transaction_status', models.CharField(default='', max_length=255, verbose_name='Card Transaction Status')),
                ('ticket_card_company_name', models.CharField(default='', max_length=255, verbose_name='Card Company')),
                ('ticket_card_old_balance', models.CharField(default='', max_length=255, verbose_name='Card Old Balance')),
                ('ticket_card_new_balance', models.CharField(default='', max_length=255, verbose_name='Card New Balance')),
                ('ticket_seat_no', models.IntegerField(default=0, verbose_name='Seat No.')),
                ('ticket_requested_at', models.IntegerField(default=0, verbose_name='Requested At')),
                ('ticket_confirmed_at', models.IntegerField(default=0, verbose_name='Confirmed At')),
            ],
            options={
                'db_table': 'tickets_external',
            },
        ),
    ]
