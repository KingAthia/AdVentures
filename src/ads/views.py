from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ads.models import Ad, AdCategory
from ads.forms import AdForm, AdPaymentForm

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
            form.save_m2m()  # Save the many-to-many relationship
            # Save selected ad categories in session for later use
            request.session['selected_ad_categories'] = [category.id for category in form.cleaned_data['adCategory']]
            request.session['ad_id'] = ad.id
            return redirect('ad_payment')  # Redirect to payment step
    else:
        form = AdForm()
    ad_categories = AdCategory.objects.all()
    context = {'form': form, 'ad_categories': ad_categories}
    return render(request, 'ads/book.html', context)

@login_required
def ad_payment(request):
    # Retrieve selected categories from the session
    ad_categories_ids = request.session.get('selected_ad_categories', [])
    ad_categories = AdCategory.objects.filter(id__in=ad_categories_ids)

    if request.method == 'POST':
        form = AdPaymentForm(request.POST, ad_categories=ad_categories)
        if form.is_valid():
            slots_data = {category.id: form.cleaned_data[f'slots_{category.id}'] for category in ad_categories}
            total_price = form.calculate_total_price(ad_categories)
            
            # Calculate subtotals for each category
            subtotals = {category.id: category.price * slots_data.get(category.id, 0) for category in ad_categories}

            # Convert data to lists for easier template processing
            categories_summary = [
                {
                    'category': category,
                    'slots': slots_data.get(category.id, 0),
                    'subtotal': subtotals.get(category.id, 0)
                }
                for category in ad_categories
            ]

            return render(request, 'ads/payment_summary.html', {
                'total_price': total_price,
                'categories_summary': categories_summary
            })
    else:
        form = AdPaymentForm(ad_categories=ad_categories)
    
    return render(request, 'ads/payment.html', {'form': form, 'ad_categories': ad_categories})

@login_required
def payment_verification(request):
    # Here you would handle the payment gateway verification
    # Simulating a successful payment verification
    payment_successful = True  # Replace with actual payment verification logic
    
    if payment_successful:
        # Retrieve payment info from session
        payment_info = request.session.get('payment_info', {})
        slots_data = payment_info.get('slots_data', {})
        ad_categories_ids = payment_info.get('ad_categories', [])

        # Save the Ad objects with the payment verified
        for category_id in ad_categories_ids:
            ad_category = AdCategory.objects.get(id=category_id)
            num_slots = slots_data.get(category_id, 0)
            for _ in range(num_slots):
                Ad.objects.create(
                    user=request.user,
                    # Other ad fields like title, image, description should be handled
                    adCategory=ad_category
                )
        
        # Clear session data after saving
        request.session.pop('selected_ad_categories', None)
        request.session.pop('payment_info', None)
        
        return render(request, 'ads/payment_success.html')
    else:
        return render(request, 'ads/payment_failed.html')