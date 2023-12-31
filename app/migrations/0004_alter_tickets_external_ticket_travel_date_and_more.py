# Generated by Django 4.0.2 on 2022-04-19 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_tickets_external_ticket_card_response_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets_external',
            name='ticket_travel_date',
            field=models.CharField(default='', max_length=255, verbose_name='Travel Date'),
        ),
        migrations.AlterField(
            model_name='tickets_external',
            name='ticket_travel_datetime',
            field=models.DateTimeField(default=None, max_length=255, verbose_name='Travel Datetime'),
        ),
        migrations.AlterField(
            model_name='tickets_external',
            name='ticket_travel_time',
            field=models.CharField(default='', max_length=255, verbose_name='Travel Time'),
        ),
    ]
