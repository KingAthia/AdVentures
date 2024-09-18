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
    def __init__(self, *args, **kwargs):
        ad_categories = kwargs.pop('ad_categories', [])
        super().__init__(*args, **kwargs)

        # Create a field for each ad category to specify the number of slots
        for category in ad_categories:
            self.fields[f'slots_{category.id}'] = forms.IntegerField(
                min_value=1, 
                label=f"Slots for {category.adCategory}",
                initial=1  # Default to 1 slot
            )

    def calculate_total_price(self, ad_categories):
        total_price = 0
        for category in ad_categories:
            num_slots = self.cleaned_data.get(f'slots_{category.id}', 0)
            total_price += category.price * num_slots
        return total_price