from django.contrib import admin

from art_project.art_portal_app.models import Painting, Style, Technique, Gallery


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'artist')
    list_filter = ('artist', 'style', 'techniques', 'gallery',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('style_name',)


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ('technique_name',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name',)
