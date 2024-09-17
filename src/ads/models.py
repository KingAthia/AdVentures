from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('BILLBOARDS','BILLBOARDS'),
    ('TAXI','TAXI'),
    ('WEBSITE','WEBSITE'),
    ('CAMPAIGNS','CAMPAIGNS'),
]

# Create your models here.
class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='staticfiles/ads/')
    description = models.TextField()
    adCategory = models.CharField(max_length=20,choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.title
