from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=500)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=3000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name

class UserProduct(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,null=False,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)

class ProductHome(models.Model):
    product_name = models.CharField(max_length=300)
    subcategory = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='shop/images', default="")
    price = models.IntegerField(default=0)
    

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

