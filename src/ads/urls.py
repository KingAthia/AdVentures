from django.urls import path
from ads.views import home, create_ad, ad_payment

urlpatterns = [
    path('', home, name='home'),
    path('book', create_ad, name='create_ad'),
    path('ad_payment/', ad_payment, name='ad_payment'),    
]