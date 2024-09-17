from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('BILLBOARDS','BILLBOARDS'),
    ('TAXI','TAXI'),
    ('WEBSITE','WEBSITE'),
    ('CAMPAIGNS','CAMPAIGNS'),
]

class AdCategory(models.Model):
    name = models.CharField(max_length=20, choices=CATEGORIES, unique=True)
    max_slots = models.PositiveIntegerField(default=10)  # Set default max slots
    
    @property
    def open_slots(self):
        # Calculate open slots dynamically
        booked_slots = self.ads.count()
        return self.total_slots - booked_slots

    def __str__(self):
        return self.name
class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='staticfiles/ads/')
    description = models.TextField()
    adCategory = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.title  

