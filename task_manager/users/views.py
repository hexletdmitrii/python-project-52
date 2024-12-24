from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.users.forms import LoginUserForm, UserRegistrationForm, UserUpdateForm


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, _("You are not allowed to perform this action."))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    extra_context = {
        'title': _("Users"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_data'] = 'some data'
        return context


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid username or password."))
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users_login')


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users_login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, _("Your account has been successfully created."))
        return super().form_valid(form)


class UserDeleteView(UserIsOwnerMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Your account has been successfully deleted."))
        return super().delete(request, *args, **kwargs)


class UserUpdateView(UserIsOwnerMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        messages.success(self.request, _("Your profile has been successfully updated."))
        return super().form_valid(form)
