from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.users.forms import LoginUserForm, UserRegistrationForm, UserUpdateForm
from django.contrib.messages.views import SuccessMessageMixin


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


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    success_message = _("Вы залогинены")

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, _("Неверное имя пользователя или пароль."))
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request):
        messages.success(request, _("Вы разлогинены"))
        return super().dispatch(request)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('users_login')
    success_message = _("Пользователь успешно зарегистрирован")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Регистрация")
        context['button'] = _("Зарегистрировать")
        context['back_url'] = reverse_lazy('users_list')
        return context


class UserDeleteView(UserIsOwnerMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'cud/delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно удален")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Delete User")
        context['back_url'] = reverse_lazy('users_list')
        context['object_del'] = self.get_object().__str__
        return context


class UserUpdateView(SuccessMessageMixin, UserIsOwnerMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'cud/create_update.html'
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно изменен")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Изменение пользователя"
        context['button'] = _("Изменить")
        context['back_url'] = reverse_lazy('users_list')
        return context
