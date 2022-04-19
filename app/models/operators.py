from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.middleware.csrf import rotate_token
from django.utils.crypto import get_random_string, salted_hmac, constant_time_compare

from app import settings
from app.data import ARRAY_GENDER


class Operators(models.Model):
    TITLE = settings.MODEL_OPERATORS_PLURAL_TITLE
    SINGULAR_TITLE = settings.MODEL_OPERATORS_SINGULAR_TITLE
    NAME = "-".join((TITLE.lower()).split())

    SESSION_KEY = '_' + TITLE.lower() + '_id'
    SESSION_MASTER_KEY = '_' + TITLE.lower() + '_'
    HASH_SESSION_KEY = '_' + TITLE.lower() + '_hash'
    REDIRECT_FIELD_NAME = 'next'

    TYPE_SUPER_ADMIN = 'super-admin'
    TYPE_ADMIN = 'admin'
    TYPE_MANAGER = 'manager'
    TYPE_OTHER = 'other'
    ARRAY_TYPE = [
        (TYPE_SUPER_ADMIN.title()).replace('-', ' '),
        (TYPE_ADMIN.title()).replace('-', ' '),
        (TYPE_MANAGER.title()).replace('-', ' '),
        (TYPE_OTHER.title()).replace('-', ' '),
    ]
    DROPDOWN_TYPE = (
        ('', '--select--'),
        (TYPE_SUPER_ADMIN, (TYPE_SUPER_ADMIN.title()).replace('-', ' ')),
        (TYPE_ADMIN, (TYPE_ADMIN.title()).replace('-', ' ')),
        (TYPE_MANAGER, (TYPE_MANAGER.title()).replace('-', ' ')),
        (TYPE_OTHER, (TYPE_OTHER.title()).replace('-', ' ')),
    )

    TEXT_STATUS_ACTIVE = 'Active'
    TEXT_STATUS_INACTIVE = 'Inactive'
    TEXT_STATUS_BLOCKED = 'Blocked'
    TEXT_STATUS_UNVERIFIED = 'Unverified'
    TEXT_STATUS_UNAPPROVED = 'Unapproved'
    STATUS_ACTIVE = 3
    STATUS_INACTIVE = 2
    STATUS_BLOCKED = 4
    STATUS_UNVERIFIED = 0
    STATUS_UNAPPROVED = 1
    ARRAY_STATUS = [
        STATUS_ACTIVE,
        STATUS_INACTIVE,
        STATUS_BLOCKED,
        STATUS_UNVERIFIED,
        STATUS_UNAPPROVED,
    ]
    ARRAY_TEXT_STATUS = [
        TEXT_STATUS_ACTIVE,
        TEXT_STATUS_INACTIVE,
        TEXT_STATUS_BLOCKED,
        TEXT_STATUS_UNVERIFIED,
        TEXT_STATUS_UNAPPROVED,
    ]
    DROPDOWN_STATUS = (
        ('', '--select--'),
        (STATUS_ACTIVE, TEXT_STATUS_ACTIVE),
        (STATUS_INACTIVE, TEXT_STATUS_INACTIVE),
        (STATUS_BLOCKED, TEXT_STATUS_BLOCKED),
        (STATUS_UNVERIFIED, TEXT_STATUS_UNVERIFIED),
        (STATUS_UNAPPROVED, TEXT_STATUS_UNAPPROVED),
    )
    HTML_TAG_STATUS_ACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_ACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Active <b></div>'
    HTML_TAG_STATUS_INACTIVE_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_INACTIVE_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Inactive <b></div>'
    HTML_TAG_STATUS_BLOCKED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_BLOCKED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Blocked <b></div>'
    HTML_TAG_STATUS_UNVERIFIED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNVERIFIED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Unverified <b></div>'
    HTML_TAG_STATUS_UNAPPROVED_COLOR = '<div class=\'center-block\' style=\'background-color:' + \
        settings.STATUS_UNAPPROVED_COLOR + \
        ';color:#FFFFFF;width:100px;text-align: center;\'><b> Unapproved <b></div>'

    operator_id = models.AutoField(SINGULAR_TITLE + ' Id', primary_key=True)
    operator_username = models.CharField(
        'Username', max_length=100, blank=False, unique=True)
    operator_auth_key = models.CharField(
        'Auth key', max_length=255, blank=False)
    operator_password = models.CharField(
        'Password', max_length=255, blank=False)
    operator_password_reset_token = models.CharField(
        'Password reset token', max_length=255, blank=True)
    operator_type = models.IntegerField(
        'type', blank=False, default=0)
    operator_company_id = models.IntegerField(
        'Company', blank=False, default=0)
    operator_first_name = models.CharField('Name', max_length=100, blank=True)
    operator_last_name = models.CharField(
        'Last Name', max_length=100, blank=True)
    operator_gender = models.IntegerField(
        'Gender', blank=False, default=0)
    operator_email_id = models.EmailField(
        'Email id', max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+250123456789'. Up to 13 digits allowed.")
    operator_phone_number = models.CharField('Phone Number',
                                             validators=[phone_regex, MinLengthValidator(10),
                                                         MaxLengthValidator(13)],
                                             max_length=13, blank=True)
    operator_address = models.CharField('Name', max_length=100, blank=True)
    operator_profile_photo = models.CharField(
        'Profile photo file path', max_length=255, blank=True)
    operator_signature = models.CharField(
        'Signature', max_length=255, blank=True)
    operator_buses = models.CharField(
        'Operator Buses', max_length=255, blank=True)
    operator_organization = models.CharField(
        'Organization', max_length=255, blank=False, default='0')
    operator_ip_address = models.CharField(
        'IP Address', max_length=100, blank=True)
    operator_created_at = models.IntegerField(
        'Created At', blank=False, default=0)
    operator_created_by = models.IntegerField(
        'Created By', blank=False, default=0)
    operator_updated_at = models.IntegerField(
        'Updated At', blank=False, default=0)
    operator_updated_by = models.IntegerField(
        'Updated By', blank=False, default=0)
    operator_status = models.IntegerField(
        'Status', blank=False, default=STATUS_UNVERIFIED)

    class Meta:
        db_table = "operators"

    def __unicode__(self):
        return self.operator_id

    def get_session_auth_hash(self):
        key_salt = "acgroup-fms.models.auth.Operators.get_session_auth_hash"
        return salted_hmac(key_salt, self.operator_password).hexdigest()

    @classmethod
    def set_redirect_field_name(cls, request, url):
        request.session[Operators.REDIRECT_FIELD_NAME] = url

    @classmethod
    def get_redirect_field_name(cls, request):
        return request.session.get(Operators.REDIRECT_FIELD_NAME, None)

    @classmethod
    def get_session_key(cls, request):
        return str(request.session[Operators.SESSION_KEY])

    @classmethod
    def login(cls, request, operator):
        session_auth_hash = ''
        if hasattr(operator, 'get_session_auth_hash'):
            session_auth_hash = operator.get_session_auth_hash()

        if Operators.SESSION_KEY in request.session:
            if cls.get_session_key(request) != operator.pk or (
                    session_auth_hash and
                    not constant_time_compare(request.session.get(Operators.HASH_SESSION_KEY, ''),
                                              session_auth_hash)):
                request.session.flush()
        else:
            request.session.cycle_key()

        request.session[Operators.SESSION_KEY] = str(operator.pk)
        request.session[Operators.SESSION_MASTER_KEY] = False
        request.session[Operators.HASH_SESSION_KEY] = session_auth_hash
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
        if Operators.SESSION_KEY in request.session:
            operator_id = request.session.get(Operators.SESSION_KEY, '0')
            try:
                operator = Operators.objects.get(operator_id=operator_id)
            except(TypeError, ValueError, OverflowError, Operators.DoesNotExist):
                operator = None
            return operator
        else:
            return None

    @classmethod
    def generate_unique_token(cls, operators, attribute):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(32)
            if operators.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token

    @classmethod
    def generate_random_number(cls, attribute, length):
        token = ''
        unique_token_found = False
        while not unique_token_found:
            token = get_random_string(length, allowed_chars='0123456789')
            if (not token.startswith('0')) and Operators.objects.filter(**{attribute: token}).count() == 0:
                unique_token_found = True
        return token
