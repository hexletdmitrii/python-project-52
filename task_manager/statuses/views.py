from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from task_manager.tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно создан")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно изменен")


class StatusDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'statuses/delete.html'
    success_message = _("Статус успешно удален")

    def form_valid(self, form):
        status = self.get_object()
        related_tasks = Task.objects.filter(status=status)

        if related_tasks.exists():
            messages.error(self.request, _(
                _("Невозможно удалить статус, так как он связан с задачами")))
            return redirect('statuses_list')
        return super().form_valid(form)
