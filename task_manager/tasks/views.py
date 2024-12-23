from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
    )
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from .models import Task
from django.views.generic import ListView
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from users.models import User


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        """
        Фильтруем задачи на основе GET-параметров.
        """
        queryset = super().get_queryset()
        selected_status = self.request.GET.get('status', '')
        selected_executor = self.request.GET.get('executor', '')
        selected_label = self.request.GET.get('label', '')
        selected_my = self.request.GET.get('my_tasks', '')

        if selected_status:
            queryset = queryset.filter(status_id=selected_status)
        if selected_executor:
            queryset = queryset.filter(executor_id=selected_executor)
        if selected_label:
            queryset = queryset.filter(labels__id=selected_label)
        if selected_my and self.request.user.is_authenticated:
            queryset = queryset.filter(executor=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительные данные в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_executor'] = self.request.GET.get('executor', '')
        context['selected_label'] = self.request.GET.get('label', '')
        context['selected_my'] = self.request.GET.get('my_tasks', '')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана.")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно обновлена.")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot delete this task.")
        return redirect('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, "Task successfully deleted.")
        return super().form_valid(form)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
