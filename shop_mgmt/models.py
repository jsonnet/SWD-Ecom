from django.db import models
from django.utils.crypto import get_random_string

from django.utils.text import slugify


# TODO check params for each key
class Partner(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    web_site = models.URLField()
    token = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        # length of 32 has a high enough entropy to get negl collisions
        self.token = get_random_string(length=32)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# TODO check params for each key
class Product(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=3, max_digits=8)
    special_price = models.DecimalField(decimal_places=3, max_digits=8, null=True, blank=True)
    count = models.IntegerField()
    image = models.URLField(null=True, blank=True)
    seller = models.CharField(max_length=22, default=0)  # 0 default, u-<id> customer, p-<id> partner

    REQUIRED_FIELDS = ['name', 'description', 'price', 'count']

    def save(self, *args, **kwargs):
        # TODO maybe make slug be uniquely created by appending pk?
        # slug auto-gen'd by name
        self.slug = slugify(self.name)

        # just set to normal price
        if self.special_price == -1:
            self.special_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
