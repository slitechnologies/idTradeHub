from django import forms
from .models import Account, UserProfile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'create password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confim password'}))
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='ZW'),
                                    required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'dob', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first_name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last_name'
        self.fields['dob'].widget.attrs['placeholder'] = 'Example 2020-12-08'
        self.fields['email'].widget.attrs['placeholder'] = 'example@mail.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter your phone_number'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm_password does not match!')


class UserForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ('Image files only')},
                                       widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
