from django.db import models

from django.utils.text import slugify


# TODO check params for each key
class Partner(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    web_site = models.URLField()
    token = models.CharField(max_length=32)

    def __str__(self):
        return self.name


# TODO check params for each key
class Product(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    slug = models.SlugField(blank=True)
    price = models.DecimalField(decimal_places=3, max_digits=8)
    special_price = models.DecimalField(decimal_places=3, max_digits=8, null=True, blank=True)
    count = models.IntegerField()
    image = models.URLField(null=True, blank=True)
    seller = models.CharField(max_length=22, default=0)  # 0 default, u-<id> customer, p-<id> partner

    REQUIRED_FIELDS = ['name', 'description', 'price', 'count']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name
