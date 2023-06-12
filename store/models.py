from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    mileage = models.IntegerField(default=0, blank=True, null=True)
    steering = models.CharField(max_length=5, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    product_model = models.CharField(max_length=50, blank=True, null=True)
    fuel = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    product_state = models.CharField(max_length=50, blank=True, null=True)
    chasis_number = models.CharField(max_length=20, blank=True, null=True)
    engine_number = models.CharField(max_length=20, blank=True, null=True)
    product_year = models.DateField(blank=True, null=True)
    product_color = models.CharField(max_length=20, blank=True, null=True)
    transmission = models.CharField(max_length=20, blank=True, null=True)
    first_registration_year = models.DateField(blank=True, null=True)
    number_of_doors = models.IntegerField(default=0, blank=True, null=True)
    number_of_seats = models.IntegerField(default=0, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    drive = models.CharField(max_length=50, blank=True, null=True)
    m_spec = models.CharField(max_length=20, blank=True, null=True)
    engine_capacity = models.CharField(max_length=20, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    max_capacity = models.CharField(max_length=20, blank=True, null=True)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    # Calculating average product star rating
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def brand(self):
        return super(VariationManager, self).filter(variation_category='brand', is_active=True)

    def fuel(self):
        return super(VariationManager, self).filter(variation_category='fuel', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
    ('brand', 'brand'),
    ('fuel', 'fuel'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.product

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='store/products_gallery', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
