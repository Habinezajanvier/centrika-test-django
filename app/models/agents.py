from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.middleware.csrf import rotate_token
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare
from decimal import Decimal

from app import settings
from app.data import ARRAY_GENDER


class Agents(models.Model):
    TITLE = settings.MODEL_AGENTS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_AGENTS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    SESSION_KEY = '_' + TITLE.lower() + '_id'
    HASH_SESSION_KEY = '_' + TITLE.lower() + '_hash'
    REDIRECT_FIELD_NAME = 'next'

    UPLOAD_PATH_AGENT_PHOTO_FILE = 'agents/photos/'
    UPLOAD_PATH_AGENT_IDENTITY_FILE = 'agents/documents/'
    AGENT_PHOTO_WIDTH = 160
    AGENT_PHOTO_HEIGHT = 160

    TYPE_NONE = 'none'
    ARRAY_TYPE = [
        (TYPE_NONE.title()).replace('-', ' '),
    ]
    DROPDOWN_TYPE = (
        ('', '--select--'),
        (TYPE_NONE, (TYPE_NONE.title()).replace('-', ' ')),
    )

    TEXT_STATUS_ACTIVE = 'Active'
    TEXT_STATUS_BLOCKED = 'Blocked'
    STATUS_ACTIVE = 1
    STATUS_BLOCKED = 0
    ARRAY_STATUS = [
        STATUS_ACTIVE,
        STATUS_BLOCKED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_BLOCKED,
        TEXT_STATUS_ACTIVE,
    ]
    DROPDOWN_STATUS = (
        ('', '--select--'),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Active <b></div>'
    HTML_TAG_STATUS_BLOCKED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Blocked <b></div>'

    agent_company = 'None'

    agent_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    agent_nid = models.CharField(
        'NID', max_length=100, blank=False, unique=True)
    agent_username = models.CharField(
        'Username', max_length=100, blank=False, unique=True)
    agent_auth_key = models.CharField(
        'Auth key', max_length=255, blank=False)
    agent_password = models.CharField(
        'Password', max_length=255, blank=False)
    agent_password_reset_token = models.CharField(
        'Password reset token', max_length=255, blank=True)
    agent_name = models.CharField(
        'Name', max_length=255, blank=False)
    agent_email_id = models.EmailField(
        'Email id', max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '0723456789'")
    agent_phone_number = models.CharField('Phone Number',
                                          validators=[phone_regex, MinLengthValidator(9),
                                                      MaxLengthValidator(20)],
                                          max_length=20, blank=True)
    agent_supervisor = models.IntegerField(
        'Supervisor', blank=False, default=0)
    agent_balance = models.DecimalField('Balance', max_digits=30, decimal_places=2,
                                        default=Decimal(0.0))
    agent_balance_card = models.DecimalField('CardBalance', max_digits=30, decimal_places=2,
                                             default=Decimal(0.0))
    agent_payment_token = models.CharField(
        'Payment Token', max_length=100, blank=False, unique=True)
    agent_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    agent_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    agent_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    agent_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    agent_status = models.IntegerField(
        'Status', blank=False, default=STATUS_ACTIVE)

    class Meta:
        db_table = "agents"

    def __unicode__(self):
        return self.agent_id

    def get_session_auth_hash(self):
        key_salt = "acgroup-rbc.models.auth.Agents.get_session_auth_hash"
        return salted_hmac(key_salt, self.agent_password).hexdigest()

    @classmethod
    def set_redirect_field_name(cls, request, url):
        request.session[Agents.REDIRECT_FIELD_NAME] = url

    @classmethod
    def get_redirect_field_name(cls, request):
        return request.session.get(Agents.REDIRECT_FIELD_NAME, None)

    @classmethod
    def get_session_key(cls, request):
        return str(request.session[Agents.SESSION_KEY])

    @classmethod
    def login(cls, request, agent):
        session_auth_hash = ''
        if hasattr(agent, 'get_session_auth_hash'):
            session_auth_hash = agent.get_session_auth_hash()

        if Agents.SESSION_KEY in request.session:
            if cls.get_session_key(request) != agent.pk or (
                    session_auth_hash and
                    not constant_time_compare(request.session.get(Agents.HASH_SESSION_KEY, ''),
                                              session_auth_hash)):
                request.session.flush()
        else:
            request.session.cycle_key()

        request.session[Agents.SESSION_KEY] = str(agent.pk)
        request.session[Agents.SESSION_MASTER_KEY] = False
        request.session[Agents.HASH_SESSION_KEY] = session_auth_hash
        # one hour session timeout
        request.session.set_expiry(3600)
        # reset csrf token
        rotate_token(request)
        return True

    @classmethod
    def logout(cls, request):
        request.session.flush()
        return True

    @classmethod
    def login_required(cls, request):
        if Agents.SESSION_KEY in request.session:
            agent_id = request.session.get(Agents.SESSION_KEY, '0')
            try:
                agent = Agents.objects.get(agent_id=agent_id)
            except(TypeError, ValueError, OverflowError, Agents.DoesNotExist):
                agent = None
            return agent
        else:
            return None

    @classmethod
    def generate_unique_token(cls, attribute):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(32)
            if Agents.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token

    @classmethod
    def generate_random_number(cls, attribute, length):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(length, allowed_chars='0123456789')
            if (not token.startswith('0')) and Agents.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token
