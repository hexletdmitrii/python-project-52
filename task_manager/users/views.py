from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as gl
from users.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from users.forms import LoginUserForm, UserRegistrationForm, UserUpdateForm
from django.views import View
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "home.html"


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    extra_context = {
        'title': gl('Users'),
    }


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверное имя пользователя или пароль.")
            return self.form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users_login')


class UserCreateView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # login(self.request, new_user)   
            # return redirect(reverse_lazy('users_list'))
            return redirect(reverse_lazy('users_login'))
        return render(request, 'users/register.html', {'form': form})


class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Проверяем, является ли текущий пользователь владельцем профиля
        if request.user != user:
            messages.error(request, "You are not allowed to delete this user.")
            return redirect('users_list')  # Перенаправление на список пользователей
        return render(request, 'users/delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Проверяем, является ли текущий пользователь владельцем профиля
        if request.user != user:
            messages.error(request, "You are not allowed to delete this user.")
            return redirect('users_list')  # Перенаправление на список пользователей
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('users_list')  # Перенаправление на список пользователей
    

class UserUpdateView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Проверяем, является ли текущий пользователь владельцем профиля
        if request.user != user:
            messages.error(request, "You are not allowed to edit this user.")
            return redirect('users_list')  # Перенаправление на список пользователей
        form = UserUpdateForm(instance=user)
        return render(request, 'users/update.html', {'form': form, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Проверяем, является ли текущий пользователь владельцем профиля
        if request.user != user:
            messages.error(request, "You are not allowed to edit this user.")
            return redirect('users_list')  # Перенаправление на список пользователей
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated.")
            return redirect('users_list')  # Перенаправление на список пользователей
        return render(request, 'users/update.html', {'form': form, 'user': user})
