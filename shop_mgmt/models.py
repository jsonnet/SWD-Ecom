from django.db import models

from django.utils.text import slugify


# TODO check params for each key
class Partner(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    web_site = models.URLField()
    token = models.CharField(max_length=32)


# TODO check params for each key
class Product(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    slug = models.SlugField()
    price = models.DecimalField(decimal_places=3, max_digits=6)
    special_price = models.DecimalField(decimal_places=3, max_digits=6)
    count = models.IntegerField()
    image = models.URLField()
    seller = models.CharField(max_length=22)  # 0 default, u-<id> customer, p-<id> partner

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
