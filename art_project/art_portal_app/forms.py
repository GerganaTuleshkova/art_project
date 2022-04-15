from django import forms

from art_project.art_portal_app.models import Painting

COLOR_CHOICES = Painting.COLOR_CHOICES


class AddPaintingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Painting
        fields = ['photo', 'title', 'style', 'techniques', 'base_material', 'width', 'height', 'price', 'gallery']

        widgets = {
            'price': forms.TextInput(
                attrs={'placeholder': 'Price must be a positive number. Currency is Euro'}),
            'width': forms.TextInput(
                attrs={'placeholder': 'in centimetres'}),
            'height': forms.TextInput(
                attrs={'placeholder': 'in centimetres'}),
        }

    main_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple,
        choices=COLOR_CHOICES,
    )


class EditPaintingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Painting
        fields = ['photo', 'title', 'style', 'techniques', 'base_material', 'width', 'height', 'price', 'gallery']

    main_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple,
        choices=COLOR_CHOICES,
    )


class DeletePaintingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Painting
        fields = ['title', 'width', 'height', 'price', 'gallery']
