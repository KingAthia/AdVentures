from django import forms
from .models import Ad, AdCategory

class AdForm(forms.ModelForm):
    adCategory = forms.ModelMultipleChoiceField(
        queryset=AdCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selection
        label="Select Ad Categories"
    )

    class Meta:
        model = Ad
        fields = ['title', 'image', 'description', 'adCategory']

    def clean_adCategory(self):
        ad_categories = self.cleaned_data['adCategory']
        for ad_category in ad_categories:
            if ad_category.open_slots <= 0:
                raise forms.ValidationError(f"No available slots for the category: {ad_category}. Please choose a different category.")
        return ad_categories
    
    
class AdPaymentForm(forms.Form):
    total_slots = forms.IntegerField(min_value=1, label="Number of Slots")

    def __init__(self, *args, **kwargs):
        self.ad_categories = kwargs.pop('initial', {}).get('ad_categories', [])
        super().__init__(*args, **kwargs)

    def calculate_total_price(self):
        total_price = 0
        for category in self.ad_categories:
            total_price += category.price * self.cleaned_data['total_slots']
        return total_price
