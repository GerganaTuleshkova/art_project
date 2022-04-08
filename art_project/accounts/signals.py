from django.core.files.storage import default_storage
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from art_project.accounts.models import Profile
from art_project.art_portal_app.models import Painting


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = User.objects.filter(pk=instance.pk)
    user.delete()


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    """Remove the file of the image after deletion except the default pic."""
    path = instance.image.name
    if path and not instance.image.name == 'profile_pics/default.png':
        default_storage.delete(path)


@receiver(post_delete, sender=Painting)
def delete_painting_photo(sender, instance, **kwargs):
    """Remove the file of the photo after deletion."""
    path = instance.photo.name
    if path:
        default_storage.delete(path)
