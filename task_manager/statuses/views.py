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
from task_manager.tasks.models import Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно создан")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Создать статус")
        context['button'] = _("Создать")
        context['back_url'] = reverse_lazy('statuses_list')
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно изменен")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update Status")
        context['button'] = _("Изменить")
        context['back_url'] = reverse_lazy('statuses_list')
        return context


class StatusDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses_list')
    template_name = 'cud/delete.html'
    success_message = _("Статус успешно удален")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Удалить статус?")
        context['back_url'] = reverse_lazy('statuses_list')
        context['object_del'] = self.get_object().__str__()
        return context

    def form_valid(self, form):
        status = self.get_object()
        related_tasks = Task.objects.filter(status=status)

        if related_tasks.exists():
            messages.error(self.request, _("Невозможно удалить статус, так как он связан с задачами!"))
            return redirect('statuses_list')
        return super().form_valid(form)


# class StatusDeleteView(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
#     model = Status
#     success_url = reverse_lazy('statuses_list')
#     template_name = 'cud/delete.html'
#     success_message = _("Статус успешно удален")

#     def test_func(self):
#         status = self.get_object()
#         related_tasks = Task.objects.filter(status=status)
#         return not related_tasks.exists()

#     def handle_no_permission(self):
#         messages.error(self.request, _("Cannot delete the status as it is linked to tasks!"))
#         return redirect('labels_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = _("Удалить статус?")
#         context['back_url'] = reverse_lazy('statuses_list')
#         context['object_del'] = self.get_object().__str__
#         return context
