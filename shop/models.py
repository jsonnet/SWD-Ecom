from django.db import models
from user_mgmt.models import UserProfile


class Payment(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    amount = models.DecimalField(decimal_places=3, max_digits=8)
    method = models.CharField(max_length=32)


class Address(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    user = models.CharField(max_length=30)  # could change relation to userprofile
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=5)
    country = models.CharField(max_length=64)
    additional_info = models.CharField(max_length=64, blank=True, null=True)


class Order(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    customer_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    placed = models.BooleanField(default=False)
    date_placed = models.DateTimeField(auto_now_add=True)
    #shipping and payment can be null initially
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)


class CartItem(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    product_id = models.CharField(max_length=64)  # could change to relation?
    quantity = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
