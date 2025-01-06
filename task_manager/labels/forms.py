from django import forms
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': _('Имя')}
