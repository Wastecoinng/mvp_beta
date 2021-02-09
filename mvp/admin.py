from django.contrib import admin
from .models import User, otp, HubLocation,EmailCollector,Notification, Transaction,RecycledItems, Manufacturer, BrandCollector

# Register your models here.
admin.site.register(User)
admin.site.register(otp)
admin.site.register(HubLocation)
admin.site.register(EmailCollector)
admin.site.register(Transaction)
admin.site.register(RecycledItems)
admin.site.register(Manufacturer)
admin.site.register(BrandCollector)
admin.site.register(Notification)