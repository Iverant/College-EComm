from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpg', upload_to='profile_pictures')
    contact_number = models.CharField(max_length=100, default='1234567890')
    mobile_number = models.CharField(max_length=15, default='1234567890')
    hostel_block = models.CharField(max_length=10, default='2')
    room_number = models.CharField(max_length=10,default='301')
    
    
    def __str__(self):
        return f"{self.user.username} - Contact: {self.contact_number}, Block: {self.hostel_block}, Room: {self.room_number}"