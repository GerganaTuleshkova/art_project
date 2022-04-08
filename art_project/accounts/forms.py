from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User

from art_project.accounts.models import Profile
from art_project.art_portal_app.models import Painting

UserModel = get_user_model()


class UserRegisterForm(auth_forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile
        fields = ['image', 'description', 'facebook_link', 'instagram_link', 'phone_number']

        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'Add a short biography of yourself', 'rows': 4}
            )
        }


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileDeleteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        # all paintings of user should be deleted as well
        paintings = Painting.objects.filter(artist_id=self.instance.pk).all()
        for p in paintings:
            p.photo.delete()
        paintings.delete()

        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'description']
