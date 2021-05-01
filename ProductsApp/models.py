from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from User.models import MerchantUser, CustomerUser
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
from ckeditor.fields import RichTextField
User = settings.AUTH_USER_MODEL

#implementing categories
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Category(MPTTModel):
    title=models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug=models.SlugField(blank=True)
    thumbnail = models.ImageField(upload_to="images/products/categories/")
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    
    def get_absolute_url(self):
        return reverse("products:category-objects", kwargs = {'slug':self.slug})
    
    def category_objects(self):
        return Products.objects.filter(is_approved=True, category=self)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Shop(models.Model):
    shop_name = models.CharField(max_length=255)
    merchant = models.OneToOneField(MerchantUser, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def shop_products(self):
        return Products.objects.filter(added_by_merchant=self.merchant)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.shop_name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:shop-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return f"{self.shop_name} - {self.merchant.user}"
    
    

class Products(models.Model):
    slug=models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # subcategories_id=models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/products/main")
    image_thumbnail = ImageSpecField(source='image',
                                   processors = [ResizeToFill(300,300)],
                                   format='JPEG',
                                   options = {'quality':100})
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    product_description=RichTextField(blank=True, null=True)
    product_long_description=RichTextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    added_by_merchant=models.ForeignKey(MerchantUser,on_delete=models.CASCADE)
    in_stock_total=models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def get_merchant_products(self):
        return Products.objects.filter(added_by_merchant=MerchantUser)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.product_name)
        return super().save(*args, **kwargs)
    
    def get_product_prices(self):
        return ShopPrice.objects.filter(product_id=self)
    
    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.product_name
    
 
class ProductDetails(models.CharField):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.product_id.product_name
    
class ProductMedia(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField(upload_to="product_media")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class ShopPrice(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    
class ProductTransaction(models.Model):
    transaction_type_choices=((1,"BUY"),(2,"SELL"))
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True) 
    
class ProductAbout(models.CharField):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class Tags(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductTags(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductQuestions(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviews(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.CharField(default="5",max_length=255)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviewVoting(models.Model):
    product_review_id=models.ForeignKey(ProductReviews,on_delete=models.CASCADE)
    user_id_voting=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductVarient(models.Model):
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
class ProductVarientItems(models.Model):
    product_varient_id=models.ForeignKey(ProductVarient,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
    def totalQuantityPrice(self):
        return self.quantity * int(self.product.product_discount_price)

class CustomerOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    def totalorderPrice(self):
        total=0
        for product in self.products.all():
            total += int(product.totalQuantityPrice())
        return total
    
class OrderAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255)
    town = models.CharField(max_length=255)    
    post_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    
    def __str__(self):
        return self.user.username
    


class OrderDeliveryStatus(models.Model):
    order_id=models.ForeignKey(CustomerOrder,on_delete=models.CASCADE)
    status=models.CharField(max_length=255)
    status_message=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    
class WishListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
    class Meta:
        verbose_name = "Wishlist item"
        verbose_name_plural = "wishlist items"
        ordering = ["-timestamp"]
        
    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    
class CustomerWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(WishListItem)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Customer Wishlist item"
        verbose_name_plural = "Customer wishlist items"
        ordering = ["-timestamp"]
    
    def __str__(self):
        return self.user.username
    
class PopularBrand(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/products/brands')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                   processors = [ResizeToFill(160,65)],
                                   format='JPEG',
                                   options = {'quality':100})
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(PopularBrand, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:brand_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
    
class ContactMessage(models.Model):
    name= models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class MpesaBaseModel(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_when = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class MpesaCalls(MpesaBaseModel):
    ip_address = models.CharField(max_length=200)
    caller = models.CharField(max_length=100)
    conversation_id = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        verbose_name = "Mpesa Call"
        verbose_name_plural = "Mpesa Calls"
        
class MpesaCallBacks(MpesaBaseModel):
    ip_address = models.CharField(max_length=200)
    caller = models.CharField(max_length=100)
    conversation_id = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        verbose_name = "Mpesa Call Back"
        verbose_name_plural = "Mpesa Call Backs"
class MpesaPayment(MpesaBaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=100)
    type = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100) 
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Mpesa Payment"
        verbose_name_plural = "Mpesa Payments"
        
    def __str__(self):
        return f"{self.first_name} - {self.amount}"
    
    
