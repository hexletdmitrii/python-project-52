from django import forms
from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import User
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
        )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password1 and password1 != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password")
        if password:
            user.set_password(password1)

        if commit:
            user.save()
        return user



