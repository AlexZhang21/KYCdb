from django.contrib import admin
from .models import Company_type,Payment,Product,Company,Receiving_bank,Tt_bank,Issuing_bank

# Register your models here.
admin.site.register(Company_type)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Receiving_bank)
admin.site.register(Tt_bank)
admin.site.register(Issuing_bank)
