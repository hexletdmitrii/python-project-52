from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Label
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


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

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Create Lable")
        context['button'] = _("Submit")
        context['back_url'] = "/labels/"
        return context


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = ("The label has been successfully updated!")

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Update Lable")
        context['button'] = _("Submit")
        context['back_url'] = "/labels/"
        return context


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'cud/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = ("The label has been successfully deleted!")

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, "Cannot delete the label as it is linked to tasks!")
            return HttpResponseRedirect(reverse_lazy('labels_list'))
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete Lable")
        context['back_url'] = "/labels/"
        context['object_del'] = self.get_object().__str__
        return context
