from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from task_manager.tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("The status has been successfully created.")

    def form_valid(self, form):
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("The status has been successfully updated.")

    def form_valid(self, form):
        return super().form_valid(form)


class StatusDeleteView(DeleteView, SuccessMessageMixin):
    model = Status
    success_url = '/statuses/'
    template_name = 'statuses/delete.html'
    success_message = _("The status has been successfully deleted.")

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        related_tasks = Task.objects.filter(status=status)
        if related_tasks.exists():
            related_tasks_list = ", ".join(str(task) for task in related_tasks)
            messages.error(
                request,
                f"Cannot delete the status as it is linked to tasks: {related_tasks_list}.")
            return HttpResponseRedirect(reverse('statuses_list'))
        return super().post(request, *args, **kwargs)
