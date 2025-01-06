from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from .filters import TaskFilter


class TaskListView(FilterView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    filterset_class = TaskFilter

    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        filterset.request = self.request
        return filterset


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Создание задачи")
        context['button'] = _("Создать")
        context['back_url'] = reverse_lazy('tasks_list')
        return context


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно изменена")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Обновление задачи")
        context['button'] = _("Изменить")
        context['back_url'] = reverse_lazy('tasks_list')
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin,
                     UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'cud/delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно удалена")

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect('tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Удалить задачу?")
        context['back_url'] = reverse_lazy('tasks_list')
        context['object_del'] = self.get_object().__str__
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
