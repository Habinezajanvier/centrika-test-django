from app.models.organizations import Organizations
from app.validators import IsPhoneNumberValidator
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    MinLengthValidator, ValidationError,
                                    validate_email, validate_integer)
from django.db.models import Q


class OrganizationSearchIndexForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(OrganizationSearchIndexForm, self).clean()
        return cleaned_data

    class Meta:
        model = Organizations
        fields = (
        )


class OrganizationCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        min_length=3,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'name',
                'aria-label': 'form-label',
            }
        ))
    email = forms.EmailField(
        label='Email Id',
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(
            5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'email',
                'aria-label': 'form-label',
            }
        ))
    phone_number = forms.CharField(
        label='Phone Number',
        min_length=9,
        max_length=13,
        validators=[MinLengthValidator(9), MaxLengthValidator(
            13), IsPhoneNumberValidator],
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'phone_number',
                'aria-label': 'form-label',
            }
        ))

    def clean_name(self):
        data = self.cleaned_data['name']
        try:
            organization = Organizations.objects.get(organization_name=data)
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            organization = None
        if organization is not None:
            raise forms.ValidationError(
                u'Name: "%s" is already in use.' % data)
        else:
            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        try:
            validate_integer(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid phone number')
        return data

    def clean(self):
        cleaned_data = super(OrganizationCreateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.operator = kwargs.pop('operator')
        self.model = kwargs.pop('model')
        super(OrganizationCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organizations
        fields = (
            'name',
            'email',
            'phone_number',
        )


class OrganizationUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        min_length=3,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'name',
                'aria-label': 'form-label',
            }
        ))
    email = forms.EmailField(
        label='Email Id',
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(
            5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'email',
                'aria-label': 'form-label',
            }
        ))
    phone_number = forms.CharField(
        label='Phone Number',
        min_length=9,
        max_length=13,
        validators=[MinLengthValidator(9), MaxLengthValidator(
            13), IsPhoneNumberValidator],
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'phone_number',
                'aria-label': 'form-label',
            }
        ))

    def clean_id(self):
        data = self.cleaned_data['id']
        print(str(data))

    def clean_name(self):
        data = self.cleaned_data['name']
        try:
            organization = Organizations.objects.get(organization_name=data)
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            organization = None
        print(str(organization.organization_id))
        print(str(self.model.organization_id))
        if organization is not None and self.model.organization_id != organization.organization_id:
            raise forms.ValidationError(
                u'Name: "%s" is already in use.' % data)
        else:
            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        try:
            validate_integer(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid phone number')
        return data

    def clean(self):
        cleaned_data = super(OrganizationUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.operator = kwargs.pop('operator')
        self.model = kwargs.pop('model')
        super(OrganizationUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organizations
        fields = (
            'name',
            'email',
            'phone_number',
        )


class OrganizationViewForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        min_length=3,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'name',
                'aria-label': 'form-label',
                'readonly': True,
                'disabled': True,
            }
        ))
    email = forms.EmailField(
        label='Email Id',
        min_length=5,
        max_length=100,
        required=True,
        validators=[MinLengthValidator(
            5), MaxLengthValidator(100), EmailValidator],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'email',
                'aria-label': 'form-label',
                'readonly': True,
                'disabled': True,
            }
        ))
    phone_number = forms.CharField(
        label='Phone Number',
        min_length=9,
        max_length=13,
        validators=[MinLengthValidator(9), MaxLengthValidator(
            13), IsPhoneNumberValidator],
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '',
                'autocomplete': 'phone_number',
                'aria-label': 'form-label',
                'readonly': True,
                'disabled': True,
            }
        ))

    def clean_name(self):
        data = self.cleaned_data['name']
        try:
            organization = Organizations.objects.get(organization_name=data)
        except(TypeError, ValueError, OverflowError, Organizations.DoesNotExist):
            organization = None
        if organization is not None and self.model.organization_id != organization.organization_id:
            raise forms.ValidationError(
                u'Name: "%s" is already in use.' % data)
        else:
            return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address')
        return data

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        try:
            validate_integer(data)
        except ValidationError:
            raise forms.ValidationError('Enter a valid phone number')
        return data

    def clean(self):
        cleaned_data = super(OrganizationUpdateForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.operator = kwargs.pop('operator')
        self.model = kwargs.pop('model')
        super(OrganizationViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Organizations
        fields = (
            'name',
            'email',
            'phone_number',
        )
