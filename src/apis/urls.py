from django.urls import path
from ads.views import home, create_ad, ad_payment, payment_verification, dashboard
from apis import views

urlpatterns = [
     # Authentication Routes
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/auth/register/', views.api_register, name='api_register'),
    
    # Ad Category Routes
    path('api/categories/', views.api_get_categories, name='api_get_categories'),
    
    # Ad Creation and Management Routes
    path('api/ads/create/', views.api_create_ad, name='api_create_ad'),
    path('api/ads/calculate-price/', views.api_calculate_ad_price, name='api_calculate_ad_price'),
    path('api/ads/payment/', views.api_process_payment, name='api_process_payment'),
    path('api/ads/user/', views.api_get_user_ads, name='api_get_user_ads'),
    
    # Additional Routes
    path('api/user/dashboard/', views.api_get_dashboard_data, name='api_get_dashboard_data'),
]