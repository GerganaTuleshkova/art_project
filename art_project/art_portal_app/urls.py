from django.urls import path

from art_project.art_portal_app.views import home_view, about_us_view, PaintingsView, PaintingDetailsView, \
    edit_painting_view, \
    add_painting_view, delete_painting_view, GalleriesView, ArtistsView, not_allowed_view, internal_error_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about-us/', about_us_view, name='about us'),

    path('paintings/', PaintingsView.as_view(), name='all paintings'),
    path('painting/details/<int:pk>/', PaintingDetailsView.as_view(), name='painting details'),
    path('painting/add/', add_painting_view, name='add painting'),
    path('painting/edit/<int:pk>/', edit_painting_view, name='edit painting'),
    path('painting/delete/<int:pk>/', delete_painting_view, name='delete painting'),

    path('galleries/', GalleriesView.as_view(), name='galleries'),

    path('artists/', ArtistsView.as_view(), name='artists'),

    path('not-allowed/', not_allowed_view, name='not allowed'),
    path('error/', internal_error_view, name='internal error'),

]
