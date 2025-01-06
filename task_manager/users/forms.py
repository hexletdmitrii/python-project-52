from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Имя пользователя'),
            'name': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Пароль'),
            'name': 'password',
        })
        self.fields['password'].label = _("Пароль")
        self.fields['username'].label = _("Имя пользователя")


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password1'}),
        label=_("Пароль")
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password2'}),
        label=_("Подтверждение пароля")
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError(_("Пароли не совпадают."))
        return cleaned_data
