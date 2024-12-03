# ads/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from ads.models import Ad, AdCategory
from ads.forms import AdForm, AdPaymentForm
import json
from decimal import Decimal

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True, 
                'user': {
                    'id': user.id, 
                    'username': user.username, 
                    'email': user.email
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        
        return JsonResponse({
            'success': True, 
            'user': {
                'id': user.id, 
                'username': user.username, 
                'email': user.email
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})

def api_get_categories(request):
    categories = AdCategory.objects.all()
    return JsonResponse({
        'categories': [
            {
                'id': category.id,
                'name': category.adCategory,
                'price': str(category.price),
                'max_slots': category.max_slots,
                'open_slots': category.open_slots
            } for category in categories
        ]
    })

@csrf_exempt
@require_http_methods(["POST"])
def api_create_ad(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        ad_form = AdForm(data)
        
        if ad_form.is_valid():
            ad = ad_form.save(commit=False)
            ad.user = request.user
            ad.save()
            ad_form.save_m2m()
            
            return JsonResponse({
                'success': True, 
                'ad': {
                    'id': ad.id,
                    'title': ad.title,
                    'description': ad.description,
                    'categories': [cat.adCategory for cat in ad.adCategory.all()]
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': ad_form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_calculate_ad_price(request):
    try:
        data = json.loads(request.body)
        category_ids = data.get('categories', [])
        slots = data.get('slots', {})
        
        categories = AdCategory.objects.filter(id__in=category_ids)
        total_price = sum(category.price * slots.get(str(category.id), 0) for category in categories)
        
        return JsonResponse({
            'success': True, 
            'total_price': str(total_price),
            'category_prices': {
                str(category.id): {
                    'name': category.adCategory,
                    'price': str(category.price),
                    'slots': slots.get(str(category.id), 0),
                    'subtotal': str(category.price * slots.get(str(category.id), 0))
                } for category in categories
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_process_payment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    
    try:
        # Simulated payment processing
        data = json.loads(request.body)
        categories = data.get('categories', [])
        slots = data.get('slots', {})
        
        # Here you would integrate with a real payment gateway
        payment_successful = True  # Simulated success
        
        if payment_successful:
            return JsonResponse({
                'success': True, 
                'message': 'Payment processed successfully',
                'categories': categories,
                'slots': slots
            })
        else:
            return JsonResponse({'success': False, 'error': 'Payment failed'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def api_get_user_ads(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    
    user_ads = Ad.objects.filter(user=request.user)
    return JsonResponse({
        'ads': [
            {
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'categories': [cat.adCategory for cat in ad.adCategory.all()],
                'created_at': ad.created_at.isoformat()
            } for ad in user_ads
        ]
    })

def api_get_dashboard_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    
    total_ads = Ad.objects.filter(user=request.user).count()
    categories = AdCategory.objects.all()
    
    return JsonResponse({
        'total_ads': total_ads,
        'categories': [
            {
                'name': category.adCategory,
                'open_slots': category.open_slots,
                'max_slots': category.max_slots
            } for category in categories
        ]
    })
