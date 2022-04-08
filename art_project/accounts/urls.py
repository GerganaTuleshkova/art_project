from django.urls import path
from django.contrib.auth import views as auth_views

from art_project.accounts.views import register, ProfileDetailsView, profile_update_view, UserLoginView, \
    ProfileDeleteView

urlpatterns = [
    path('register/', register, name='register'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts_templates/logout.html'), name='logout'),

    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/update/', profile_update_view, name='update profile'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='delete profile'),
]
