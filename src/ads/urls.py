from django.urls import path
from ads.views import home

urlpatterns = [
    path('', home, name='home'),    
]