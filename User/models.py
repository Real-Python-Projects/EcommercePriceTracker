from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.conf import settings


User = settings.AUTH_USER_MODEL
# Create your models here.

STAFF_CHOICES = [
    ("CEO", "CEO"),
    ("Marketing Officer", "Marketing Officer"),
    ("Customer Care","Customer Care"),
    ("Quality Officer", "Quality Officer")
]

class CustomUser(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    
    
class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/admin")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(100,100)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class StaffUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/staff")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(400,400)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    position = models.CharField(choices=STAFF_CHOICES, max_length=255)
    description = models.TextField(default="No description")
    created_at = models.DateTimeField(auto_now_add=True)
    list_on_about = models.BooleanField(default=False)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    linked_in = models.CharField(max_length=255, blank=True, null=True)
    google_plus = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class MerchantUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/merchant")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(100,100)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class CustomerUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/customer")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(100,100)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="images/profile/customer", default="images/profile/default-profile.jpg")
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(100,100)],
                                           format='JPEG',
                                           options={'quality':100}
                                           )
    phone = models.CharField(max_length=13)
    
    
    def __str__(self):
        return self.user.username
    
class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    otp = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone} - {self.user.username}"
    
    
class EmailSubscibers(models.Model):
    email = models.EmailField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    def no_of_subscribers(self):
        return self.objects.all().count()
    
    
class BestCustomerReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic_thumbnail = ImageSpecField(source='user.profile_pic_thumbnail')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Best Customer Review"
        verbose_name_plural = "Best Customer Reviews"
        
    def __str__(self):
        return self.user.username
    