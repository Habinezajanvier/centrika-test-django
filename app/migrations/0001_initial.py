# Generated by Django 3.2.4 on 2021-09-12 09:37

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access_Permissions',
            fields=[
                ('access_permission_name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Access Permission Name')),
                ('access_permission_details', models.CharField(blank=True, max_length=255, verbose_name='Details')),
                ('access_permission_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
            ],
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
            name='Operators',
            fields=[
                ('operator_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Operator Id')),
                ('operator_type', models.CharField(choices=[('', '--select--'), ('super-admin', 'Super Admin'), ('admin', 'Admin'), ('manager', 'Manager'), ('other', 'Other')], default='other', max_length=20, verbose_name='Type')),
                ('operator_username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('operator_auth_key', models.CharField(max_length=255, verbose_name='Auth key')),
                ('operator_password_hash', models.CharField(max_length=255, verbose_name='Password')),
                ('operator_password_reset_token', models.CharField(blank=True, max_length=255, verbose_name='Password reset token')),
                ('operator_name', models.CharField(max_length=100, verbose_name='Name')),
                ('operator_gender', models.CharField(choices=[('', '--select--'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='', max_length=6, verbose_name='Gender')),
                ('operator_contact_phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+250123456789'. Up to 13 digits allowed.", regex='^\\+?1?\\d{9,15}$'), django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(13)], verbose_name='Phone Number')),
                ('operator_contact_email_id', models.EmailField(blank=True, max_length=100, verbose_name='Email id')),
                ('operator_profile_photo_file_path', models.CharField(blank=True, max_length=255, verbose_name='Profile photo file path')),
                ('operator_organization_id', models.IntegerField(default=0, verbose_name='Organization')),
                ('operator_created_at', models.IntegerField(default=0, verbose_name='Created At')),
                ('operator_created_by', models.IntegerField(default=0, verbose_name='Created By')),
                ('operator_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('operator_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('operator_status', models.IntegerField(default=3, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Operator_Access_Permissions',
            fields=[
                ('operator_access_permission_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('operator_access_permission_updated_at', models.IntegerField(default=0, verbose_name='Updated At')),
                ('operator_access_permission_updated_by', models.IntegerField(default=0, verbose_name='Updated By')),
                ('access_permissions_access_permission_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.access_permissions')),
                ('operators_operator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.operators')),
            ],
        ),
    ]
