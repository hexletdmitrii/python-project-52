import django_filters
from .models import Task, Status


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),  # Получаем все статусы из модели Status
        # widget=forms.Select(attrs={
        #     'class': 'form-select ml-2 mr-3'  # Класс для стилизации
        # }),
        label="Status"
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
