from django.contrib import admin

# Register your models here.
from .models import Product, Contact, UserProduct ,ProductHome

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(UserProduct)
admin.site.register(ProductHome)

