from django.db import models
from user_mgmt.models import UserProfile

#P4
#TODO discuss if Cascade is best option for deletion

class Payment(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    amount = models.IntegerField()
    method = models.CharField(max_length=32)

class Address(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    user = models.CharField(max_length=30)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    additional_info = models.CharField(max_length=64)

class Order(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    customer_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    placed = models.BooleanField(default=False)
    date_placed = models.DateTimeField()
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

class CartItem(models.Model):
    pk_x = models.AutoField(primary_key=True, db_column='pk')  # pk is a reserved word in python!
    product_id = models.CharField(max_length=64)
    quantity = models.IntegerField()
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)


