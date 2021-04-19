from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from  django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    
    def CategoryItems(self):
        return Blog.objects.filter(category=self)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='images/blog/')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(370,347)],
                                     format='jpeg',
                                     options={'quality':100})
    img_detail_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(1170,555)],
                                     format='webp',
                                     options={'quality':100})
    added_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title+self.author.username)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={"slug": self.slug, 'pk':self.pk})