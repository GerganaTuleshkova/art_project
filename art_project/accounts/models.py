from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from PIL import Image



UserModel = get_user_model()
#
#
# class OnartUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
#     USERNAME_MAX_LENGTH = 25
#
#     username = models.CharField(
#         max_length=USERNAME_MAX_LENGTH,
#         unique=True,
#     )
#
#     date_joined = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     is_staff = models.BooleanField(
#         default=False,
#     )
#
#     USERNAME_FIELD = 'username'
#
#     objects = OnartUserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        # auth_models.User,
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        )

    first_name = models.CharField(
        max_length=150,
    )

    last_name = models.CharField(
        max_length=150,
    )

    image = models.ImageField(
        default='profile_pics/default.png',
        upload_to='profile_pics',
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    facebook_link = models.URLField(
        blank=True,
        null=True,
    )
    instagram_link = models.URLField(
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(13),
            RegexValidator(regex=r'^\+?1?\d{9,15}$',
                           message='Phone number must be entered in the format: "+999999999". '
                                   'Exactly 12 digits is allowed.')
        ]
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return 'Unknown Artist'
