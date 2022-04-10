from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Model
from django.shortcuts import render, redirect
from django.views import generic as views

from art_project.accounts.models import Profile
from art_project.art_portal_app.forms import EditPaintingForm, AddPaintingForm, DeletePaintingForm
from art_project.art_portal_app.models import Painting, Gallery, Style

UserModel = get_user_model()

"""General views"""


def home_view(request):
    return render(request, 'art_portal_templates/home.html')


def about_us_view(request):
    return render(request, 'art_portal_templates/about.html')


def not_allowed_view(request):
    return render(request, 'art_portal_templates/not_allowed.html')


def internal_error_view(request):
    return render(request, 'art_portal_templates/error.html')


"""Paintings views"""


class PaintingsView(views.ListView):
    model = Painting
    template_name = 'art_portal_templates/paintings.html'
    context_object_name = 'paintings'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['styles'] = Style.objects.all()
        return context

    def get_queryset(self):
        paintings = super().get_queryset()
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        paintings = paintings.filter(style__style_name__istartswith=q)
        return paintings


class PaintingDetailsView(views.DetailView):
    template_name = 'art_portal_templates/painting_details.html'
    model = Painting
    context_object_name = 'painting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_author'] = self.object.artist == self.request.user

        return context


@login_required()
def add_painting_view(request):
    profile = UserModel.profile
    if request.method == 'POST':
        form = AddPaintingForm(request.POST, request.FILES, instance=Painting(artist=request.user))
        if form.is_valid():
            instance = form.save()
            return redirect('painting details', instance.pk)
    else:
        form = AddPaintingForm()
    context = {
        'form': form,
    }
    return render(request, 'art_portal_templates/add_painting.html', context)


def edit_painting_view(request, pk):
    painting = Painting.objects.get(pk=pk)

    if not request.user.pk == painting.artist.pk:
        return redirect('not allowed')

    if request.method == 'POST':
        form = EditPaintingForm(request.POST, request.FILES, instance=painting)
        if form.is_valid():
            form.save()
            return redirect('painting details', painting.pk)
    else:
        form = EditPaintingForm(instance=painting)
    context = {
        'form': form,
        'painting': painting,
    }
    return render(request, 'art_portal_templates/edit_painting.html', context)


def delete_painting_view(request, pk):
    painting = Painting.objects.get(pk=pk)

    user = get_user_model()

    if not request.user.pk == painting.artist.pk:
        return redirect('not allowed')
    if request.method == 'POST':
        form = DeletePaintingForm(request.POST, instance=painting)
        if form.is_valid():
            form.save()
            return redirect('profile details', request.user.pk)
    else:
        form = DeletePaintingForm(instance=painting)
    context = {
        'form': form,
        'painting': painting,
    }
    return render(request, 'art_portal_templates/delete_painting.html', context)


"""Galleries view"""


class GalleriesView(views.ListView):
    model = Gallery
    template_name = 'art_portal_templates/galleries.html'
    context_object_name = 'galleries'


"""Artists Views"""


class ArtistsView(views.ListView):
    model = Profile
    template_name = 'art_portal_templates/artists.html'
    context_object_name = 'artists'
    paginate_by = 6

    def get_queryset(self):
        artists_query_set = super().get_queryset()
        paintings = Painting.objects.prefetch_related('artist')

        artists_with_paintings = []
        for artist in artists_query_set:
            paintings_of_author = paintings.filter(artist_id=artist.pk)
            if len(paintings_of_author) > 0:
                artists_with_paintings.append(artist.pk)
        result = artists_query_set.filter(pk__in=artists_with_paintings)
        return result
