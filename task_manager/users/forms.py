from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from task_manager.users.models import User


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
        self.fields['username'].label = "Имя пользователя"


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password1'}),
        label="Пароль"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password2'}),
        label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
