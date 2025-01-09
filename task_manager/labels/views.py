from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Label
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from .forms import LabelForm


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно создана")


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно изменена")


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels_list')
    template_name = 'labels/delete.html'
    success_message = _("Метка успешно удалена")

    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, _(
                "Невозможно удалить метку, так как она связана с задачами!"))
            return redirect('labels_list')
        return super().form_valid(form)
