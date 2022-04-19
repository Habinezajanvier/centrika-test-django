from decimal import Decimal

from app import settings
from django.db import models


class Agent_Floats_Cards(models.Model):
    TITLE = settings.MODEL_AGENT_FLOATS_CARDS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_AGENT_FLOATS_CARDS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    TEXT_TYPE_DEFAULT = 'None'
    TEXT_TYPE_REMOVE = 'Remove'
    TEXT_TYPE_ADD = 'Add'
    TYPE_DEFAULT = 0
    TYPE_REMOVE = 1
    TYPE_ADD = 2
    ARRAY_TYPE = [
        TYPE_DEFAULT,
        TYPE_REMOVE,
        TYPE_ADD,
    ]
    TEXT_ARRAY_TYPE = [
        TEXT_TYPE_DEFAULT,
        TEXT_TYPE_REMOVE,
        TEXT_TYPE_ADD,
    ]
    DROPDOWN_TYPE = (
        ('', '--select--'),
        (TYPE_DEFAULT, TEXT_TYPE_DEFAULT),
        (TYPE_REMOVE, TEXT_TYPE_REMOVE),
        (TYPE_ADD, TEXT_TYPE_ADD),
    )

    TEXT_ACTION_DEFAULT = 'Request'
    TEXT_ACTION_DEFAULT_REFUND = 'Refund (Request)'
    TEXT_ACTION_TRANSFER = 'Transfer'
    TEXT_ACTION_TRANSFER_REFUND = 'Refund (Transfer)'
    TEXT_ACTION_TICKET_BOOK = 'Book-Ticket'
    TEXT_ACTION_TICKET_BOOK_REFUND = 'Refund (Book-Ticket)'
    TEXT_ACTION_CARD_TOPUP = 'Card-Topup'
    TEXT_ACTION_CARD_TOPUP_REFUND = 'Refund (Card-Topup)'
    DROPDOWN_ACTION = (
        ('', '--select--'),
        (TEXT_ACTION_DEFAULT, TEXT_ACTION_DEFAULT),
        (TEXT_ACTION_DEFAULT_REFUND, TEXT_ACTION_DEFAULT_REFUND),
        (TEXT_ACTION_TRANSFER, TEXT_ACTION_TRANSFER),
        (TEXT_ACTION_TRANSFER_REFUND, TEXT_ACTION_TRANSFER_REFUND),
        (TEXT_ACTION_TICKET_BOOK, TEXT_ACTION_TICKET_BOOK),
        (TEXT_ACTION_TICKET_BOOK_REFUND, TEXT_ACTION_TICKET_BOOK_REFUND),
        (TEXT_ACTION_CARD_TOPUP, TEXT_ACTION_CARD_TOPUP),
        (TEXT_ACTION_CARD_TOPUP_REFUND, TEXT_ACTION_CARD_TOPUP_REFUND),
    )

    TEXT_STATUS_PENDING = 'Pending'
    TEXT_STATUS_APPROVED = 'Approved'
    TEXT_STATUS_DENIED = 'Denied'
    STATUS_PENDING = 1
    STATUS_APPROVED = 2
    STATUS_DENIED = 0
    ARRAY_STATUS = [
        STATUS_PENDING,
        STATUS_APPROVED,
        STATUS_DENIED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_DENIED,
        TEXT_STATUS_PENDING,
        TEXT_STATUS_APPROVED,
    ]
    DROPDOWN_STATUS = (
        ('', '--select--'),
        (STATUS_PENDING, TEXT_STATUS_PENDING),
        (STATUS_APPROVED, TEXT_STATUS_APPROVED),
        (STATUS_DENIED, TEXT_STATUS_DENIED),
    )
    HTML_TAG_STATUS_APPROVED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Approved <b></div>'
    HTML_TAG_STATUS_DENIED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_INACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Denied <b></div>'
    HTML_TAG_STATUS_PENDING_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Pending <b></div>'

    HTML_TAG_TYPE_DEFAULT_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNVERIFIED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> None <b></div>'
    HTML_TAG_TYPE_REMOVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNVERIFIED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Remove <b></div>'
    HTML_TAG_TYPE_ADD_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNVERIFIED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Add <b></div>'

    agent_float_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    agent_float_agent_id = models.IntegerField(
        'Agent', blank=False, default=0)
    agent_float_agent_name = models.CharField(
        'Agent', max_length=255, blank=True)
    agent_float_type = models.IntegerField(
        'Type', blank=False, default=TYPE_DEFAULT)
    agent_float_bill = models.CharField(
        'Bill', max_length=255, blank=False, default=None, unique=True)
    agent_float_amount = models.DecimalField('Amount', max_digits=30, decimal_places=2,
                                             default=Decimal(0.0))
    agent_float_old_balance = models.DecimalField('Old Balance', max_digits=30, decimal_places=2,
                                                  default=Decimal(0.0))
    agent_float_new_balance = models.DecimalField('New Balance', max_digits=30, decimal_places=2,
                                                  default=Decimal(0.0))
    agent_float_reason = models.CharField('Reason', max_length=255, blank=True)
    agent_float_action = models.CharField('Action', max_length=255, blank=True)
    agent_float_action_id = models.IntegerField(
        'Action Id', blank=False, default=0)
    agent_float_action_refund = models.IntegerField(
        'Refund', blank=False, default=0)
    agent_float_action_refund_id = models.IntegerField(
        'Refund Id', blank=False, default=0)
    agent_float_ticket_id = models.IntegerField(
        'Ticket Id', blank=False, default=0)
    agent_float_company_id = models.IntegerField(
        'Company Id', blank=False, default=0)
    agent_float_company_name = models.CharField(
        'Company', max_length=255, blank=True)
    agent_float_transaction_id = models.IntegerField(
        'Transaction Id', blank=False, default=0)
    agent_float_card_id = models.IntegerField(
        'Card Id', blank=False, default=0)
    agent_float_card_number = models.CharField(
        'Card Number', max_length=255, blank=True)
    agent_float_card_old_balance = models.CharField(
        'Card Old Balance', max_length=255, blank=True)
    agent_float_card_new_balance = models.CharField(
        'Card New Balance', max_length=255, blank=True)
    agent_float_customer_id = models.IntegerField(
        'Customer Id', blank=False, default=0)
    agent_float_customer_name = models.CharField(
        'Customer Name', max_length=255, blank=True)
    agent_float_customer_phone_number = models.CharField(
        'Customer Phone Number', max_length=255, blank=True)
    agent_float_requested_at = models.IntegerField(
        'Created At', blank=False, default=0)
    agent_float_requested_by = models.IntegerField(
        'Created By', blank=False, default=0)
    agent_float_requested_md = models.IntegerField(
        'Created Md', blank=False, default=0)
    agent_float_requested_by_name = models.CharField(
        'Created By', max_length=255, blank=True)
    agent_float_approval_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    agent_float_approval_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    agent_float_approval_updated_md = models.IntegerField(
        'Updated Md', blank=False, default=0)
    agent_float_approval_updated_by_name = models.CharField(
        'Updated By', max_length=255, blank=True)
    agent_float_status = models.IntegerField(
        'Status', blank=False, default=STATUS_PENDING)
    agent_float_bank_reference = models.CharField('Bank Reference', max_length=255, blank=True)

    class Meta:
        db_table = "agent_card_floats"
