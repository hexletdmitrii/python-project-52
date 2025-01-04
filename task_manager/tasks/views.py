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
    success_message = _("The task has been successfully created.")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create Task")
        context['button'] = _("Submit")
        context['back_url'] = "/tasks/"
        return context


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("The task has been successfully updated.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update Task")
        context['button'] = _("Submit")
        context['back_url'] = reverse_lazy('tasks_list')
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'cud/delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Task successfully deleted.")

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot delete this task.")
        return redirect('tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete Task")
        context['back_url'] = "/tasks/"
        context['object_del'] = self.get_object().__str__
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
