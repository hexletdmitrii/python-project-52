from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from task_manager.users.models import User
from django.core.exceptions import ValidationError


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


class UserUpdateForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        fields = ['username', 'first_name', 'last_name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password_confirm'].required = False
