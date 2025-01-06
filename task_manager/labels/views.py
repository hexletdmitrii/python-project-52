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
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно создана")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Создать метку")
        context['button'] = _("Создать")
        context['back_url'] = reverse_lazy('labels_list')
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно изменена")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Изменить метку")
        context['button'] = _("Изменить")
        context['back_url'] = reverse_lazy('labels_list')
        return context


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels_list')
    template_name = 'cud/delete.html'
    success_message = _("Метка успешно удалена")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Удалить Метку?")
        context['back_url'] = reverse_lazy('labels_list')
        context['object_del'] = self.get_object().__str__()
        return context

    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, _(
                "Невозможно удалить метку, так как она связана с задачами!"))
            return redirect('labels_list')
        return super().form_valid(form)
