from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from tasks.models import Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан.")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно обновлен.")
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    model = Status
    success_url = '/statuses/'
    template_name = 'statuses/delete.html'

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        related_tasks = Task.objects.filter(status=status)
        if related_tasks.exists():
            related_tasks_list = ", ".join(str(task) for task in related_tasks)
            messages.error(
                request,
                f"Невозможно удалить статус, так как он связан с задачами: {related_tasks_list}.")
            return HttpResponseRedirect(reverse('statuses_list'))
        return super().post(request, *args, **kwargs)
