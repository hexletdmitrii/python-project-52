from django import forms
from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'name': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль',
            'name': 'password',
        })
        self.fields['password'].label = "Пароль"


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False,
    )
    password_confirm = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password_confirm = cleaned_data.get("password_confirm")

        if password1 and password1 != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user
