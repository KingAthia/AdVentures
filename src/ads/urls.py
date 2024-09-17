from django.urls import path
from ads.views import home, create_ad

urlpatterns = [
    path('', home, name='home'),
    path('book', create_ad, name='create_ad'),    
]