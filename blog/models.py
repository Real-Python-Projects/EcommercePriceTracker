from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from  django.utils.text import slugify
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()
#implementing categories
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class BlogCategory(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(blank=True)
    
    def CategoryItems(self):
        return Blog.objects.filter(category=self)
    
    def __str__(self):
        return self.name
    class MPTTMeta:
        order_insertion_by = ['name']
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
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/blog/')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(1024,610)],
                                     format='jpeg',
                                     options={'quality':100})
    small_image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(200,200)],
                                     format='jpeg',
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
    
    def no_of_comments(self):
        return Comments.objects.filter(post=self).count()
    
    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={"slug":self.slug, 'pk':self.pk})
    
class BlogMedia(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to="images/blog/detail")
    image_thumbnail = ImageSpecField(source='post_image',
                                    processors=[ResizeToFill(1024,610)],
                                    format='jpeg',
                                    options={'quality':100})
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Comments(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    
    
    