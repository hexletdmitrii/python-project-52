from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Label
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = ("The label has been successfully created!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create Lable")
        context['button'] = _("Submit")
        context['back_url'] = reverse_lazy('labels_list')
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = ("The label has been successfully updated!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update Lable")
        context['button'] = _("Submit")
        context['back_url'] = reverse_lazy('labels_list')
        return context


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Label
    template_name = 'cud/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("The label has been successfully deleted!")

    def test_func(self):
        label = self.get_object()
        return not label.tasks.exists()

    def handle_no_permission(self):
        messages.error(self.request, _("Cannot delete the label as it is linked to tasks!"))
        return redirect('labels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete Label")
        context['back_url'] = reverse_lazy('labels_list')
        context['object_del'] = self.get_object().__str__
        return context
