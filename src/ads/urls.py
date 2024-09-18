from django.urls import path
from ads.views import home, create_ad, ad_payment, payment_verification, dashboard

urlpatterns = [
    path('', home, name='home'),
    path('book', create_ad, name='create_ad'),
    path('ad_payment/', ad_payment, name='ad_payment'),
    path('payment_verification', payment_verification, name='payment_verification'),
    path('dashboard/', dashboard, name='dashboard'),    
]