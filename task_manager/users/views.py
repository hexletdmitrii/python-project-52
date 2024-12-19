from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from users.models import User
from users.forms import LoginUserForm, UserRegistrationForm, UserUpdateForm


# Миксин для проверки прав доступа
class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            messages.error(request, _("You are not allowed to perform this action."))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


# Главная страница
class HomeView(TemplateView):
    template_name = "home.html"


# Список пользователей
class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    extra_context = {
        'title': _("Users"),
    }

    def get_context_data(self, **kwargs):
        # Вызовите родительский метод, чтобы получить стандартный контекст
        context = super().get_context_data(**kwargs)
        # Добавьте свои данные в контекст
        context['extra_data'] = 'some data'
        return context

# Вход в систему
class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid username or password."))
        return super().form_invalid(form)


# Выход из системы
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users_login')


# Регистрация пользователя
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


# Удаление пользователя
class UserDeleteView(UserIsOwnerMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Your account has been successfully deleted."))
        return super().delete(request, *args, **kwargs)


# Обновление профиля пользователя
class UserUpdateView(UserIsOwnerMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        messages.success(self.request, _("Your profile has been successfully updated."))
        return super().form_valid(form)
