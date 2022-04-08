from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib.auth import forms as auth_forms, authenticate, login
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import UpdateView

from art_project.accounts.forms import UserRegisterForm, ProfileUpdateForm, ProfileDeleteForm, UserUpdateForm
from art_project.accounts.models import Profile
from art_project.art_portal_app.models import Painting


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile details', user.pk)
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts_templates/register.html', context)


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts_templates/login.html'
    # success_url = reverse_lazy('home') # --> not needed because of settings.py/LOGIN_REDIRECT_URL


# can be viewed by all users, authentication is not required
class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'accounts_templates/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # self.object is a Profile
        paintings = Painting.objects.filter(artist=self.object.user)
        paintings_count = len(paintings)

        context['paintings_count'] = paintings_count
        context['paintings'] = paintings
        context['is_owner'] = self.object.user == self.request.user
        return context


def profile_update_view(request):
    profile_pk = request.user.pk
    profile = Profile.objects.get(pk=profile_pk)
    user = request.user

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if p_form.is_valid() and u_form.is_valid:
            user = u_form.save()
            profile = p_form.save()
            profile.first_name = u_form.cleaned_data.get('first_name')
            profile.last_name = u_form.cleaned_data.get('last_name')
            profile.email = u_form.cleaned_data.get('email')
            user.save()
            profile.save()
            # p_form.save()
            # u_form.save()
            return redirect('profile details', profile.pk)
    else:
        p_form = ProfileUpdateForm(instance=profile)
        u_form = UserUpdateForm(instance=user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
        'profile': profile,
    }
    return render(request, 'accounts_templates/update_profile.html', context)


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileDeleteForm
    template_name = 'accounts_templates/delete_profile.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('home')

    def test_func(self):
        profile = self.get_object()
        if self.request.user.pk == profile.pk:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect('not allowed')
        return super().dispatch(request, *args, **kwargs)
