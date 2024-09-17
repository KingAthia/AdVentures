from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ads.models import Ad, AdCategory
from ads.forms import AdForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')  # Replace with your redirect view
    else:
        form = AdForm()
    ad_categories = AdCategory.objects.all()
    return render(request, 'create_ad.html', {'form': form, 'ad_categories': ad_categories})
