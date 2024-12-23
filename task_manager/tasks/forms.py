from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'status': 'Status',
            'executor': 'Executor',
            'labels': 'Lable'
        }
