import django_filters
from .models import Task, Status
from django import forms


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус"
    )
    my_tasks = django_filters.BooleanFilter(
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
        label="Только свои задачи"
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        labels = {
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метка'
        }

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset


