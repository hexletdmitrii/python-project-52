from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("The status has been successfully created.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create Status")
        context['button'] = _("Submit")
        context['back_url'] = reverse_lazy('statuses_list')
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("The status has been successfully updated.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update Status")
        context['button'] = _("Submit")
        context['back_url'] = reverse_lazy('statuses_list')
        return context


class StatusDeleteView(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'cud/delete.html'
    success_message = _("The status has been successfully deleted.")

    def test_func(self):
        status = self.get_object()
        related_tasks = Task.objects.filter(status=status)
        return not related_tasks.exists()

    def handle_no_permission(self):
        messages.error(self.request, _("Cannot delete the status as it is linked to tasks!"))
        return redirect('labels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete Status")
        context['back_url'] = reverse_lazy('statuses_list')
        context['object_del'] = self.get_object().__str__
        return context
