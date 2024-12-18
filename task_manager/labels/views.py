from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Label
from tasks.models import Task
class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана!")
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно обновлена!")
        return super().form_valid(form)

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, "Невозможно удалить метку, так как она связана с задачами!")
            return HttpResponseRedirect(reverse_lazy('labels_list'))
        messages.success(self.request, "Метка успешно удалена!")
        return super().post(request, *args, **kwargs)
