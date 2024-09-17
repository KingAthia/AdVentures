from django import forms
from .models import Ad, AdCategory

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'image', 'description', 'adCategory']

    def clean_adCategory(self):
        ad_category = self.cleaned_data['adCategory']
        if ad_category.open_slots <= 0:
            raise forms.ValidationError(f"No available slots for the category: {ad_category}. Please choose a different category.")
        return ad_category