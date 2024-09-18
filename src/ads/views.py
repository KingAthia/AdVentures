from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ads.models import Ad, AdCategory
from ads.forms import AdForm, AdPaymentForm
from decimal import Decimal

# Create your views here.
def home(request):
    return render(request, 'index.html')

# Function to convert Decimal objects to strings in a dictionary
def convert_decimals_to_strings(data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = str(value)
        elif isinstance(value, dict):
            convert_decimals_to_strings(value)
    return data

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            # Save the ad object in session instead of saving to the database
            request.session['ad_data'] = {
                'title': ad.title,
                'description': ad.description,
                'image': ad.image.url if ad.image else None,
                'adCategory': [category.id for category in form.cleaned_data['adCategory']]
            }
            request.session['selected_ad_categories'] = [category.id for category in form.cleaned_data['adCategory']]
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

            # Prepare summary for display
            categories_summary = [
                {
                    'category': category,
                    'slots': slots_data.get(category.id, 0),
                    'subtotal': subtotals.get(category.id, 0)
                }
                for category in ad_categories
            ]

            # Save payment info in session for later use
            payment_info = {
                'slots_data': slots_data,
                'ad_categories': ad_categories_ids,
                'total_price': total_price
            }
            # Convert Decimal objects to strings before storing in session
            request.session['payment_info'] = convert_decimals_to_strings(payment_info)

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

        # Retrieve ad data from session
        ad_data = request.session.get('ad_data', {})
        
        # Save the Ad object with the payment verified
        ad = Ad(
            user=request.user,
            title=ad_data.get('title'),
            description=ad_data.get('description'),
            image=ad_data.get('image')
        )
        ad.save()
        ad.adCategory.set(AdCategory.objects.filter(id__in=ad_data.get('adCategory', [])))
        ad.save()

        # Clear session data after saving
        request.session.pop('selected_ad_categories', None)
        request.session.pop('payment_info', None)
        request.session.pop('ad_data', None)
        
        return render(request, 'ads/payment_success.html')
    else:
        return render(request, 'ads/payment_failed.html')