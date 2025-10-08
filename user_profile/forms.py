from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

            if field_name == "bio":
                existing_styles = field.widget.attrs.get('style', '')
                field.widget.attrs['style'] = (existing_styles + ' resize: none;').strip()
            