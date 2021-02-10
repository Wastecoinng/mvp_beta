from django.db import models
from django.utils import timezone
import datetime

# USER
class User(models.Model):
    class Meta:
        db_table = "user_table"
    user_id = models.CharField(max_length=500,unique=True)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    user_phone = models.TextField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    user_address = models.TextField(max_length=200,verbose_name="Address")
    user_state = models.TextField(max_length=200,verbose_name="State")
    user_council_area = models.TextField(max_length=200,verbose_name="LGA/Council Area")
    user_country = models.TextField(max_length=200,verbose_name="Country")
    minedCoins = models.FloatField(verbose_name="minedCoins",default=0)
    totalRecyled = models.IntegerField(verbose_name="Total plastics recycled",default=100)
    totalDelivered = models.IntegerField(verbose_name="Total plastics Delivered",default=0)
    totalNotDelivered = models.IntegerField(verbose_name="Total plastics not Delivered",default=0)
    # newly added
    account_name = models.TextField(max_length=150,verbose_name="Account Name",default="Null")
    account_number = models.TextField(max_length=150,verbose_name="Account Number",default="Null")
    bank_name = models.TextField(max_length=150,verbose_name="Bank Name",default="Null")
    date_added = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user_id} - {self.firstname} - {self.lastname} - {self.email} - {self.user_phone} - {self.user_address}- {self.user_state} - {self.user_council_area} - {self.user_country} - {self.date_added} - {self.account_name} - {self.account_number} - {self.bank_name} - {self.minedCoins}"

# HUB AGENTS
class Hub_User(models.Model):
    class Meta:
        db_table = "hub_user_table"
    hub_id = models.CharField(max_length=500,unique=True)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    hub_phone = models.TextField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    hub_password = models.TextField(max_length=200,verbose_name="Password")
    hub_address = models.TextField(max_length=200,verbose_name="Address")
    hub_state = models.TextField(max_length=200,verbose_name="State")
    hub_council_area = models.TextField(max_length=200,verbose_name="LGA/Council Area")
    hub_country = models.TextField(max_length=200,verbose_name="Country")
    total_items_collected = models.FloatField(verbose_name="Total Plastics collected",default=0)
    date_added = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.hub_id} - {self.firstname} - {self.lastname} - {self.email} - {self.hub_phone} - {self.hub_address}- {self.hub_state} - {self.hub_council_area} - {self.hub_country} - {self.date_added} - {self.total_items_collected}"

class otp(models.Model):
    class Meta:
        db_table = "OTP_Code"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.TextField(max_length=20,verbose_name="OTP CODE")
    validated = models.BooleanField(default=False)
    password_reset_code = models.TextField(max_length=20,verbose_name="Reset Code",default="")
    date_added = models.DateTimeField(default=timezone.now)

class HubLocation(models.Model):
    class Meta:
        db_table = "hub_locations"
    hub_name = models.TextField(max_length=100,verbose_name="Hub Name")
    longitude = models.TextField(max_length=90,verbose_name="Longitude")
    latitute = models.TextField(max_length=90,verbose_name="Latitute")
    hub_address = models.TextField(max_length=200,verbose_name="Address")
    hub_state = models.TextField(max_length=200,verbose_name="State")
    hub_council_area = models.TextField(max_length=200,verbose_name="LGA/Council Area")
    hub_country = models.TextField(max_length=200,verbose_name="Country")
    date_added = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.hub_name} - {self.longitude} - {self.latitute} - {self.hub_address} - {self.hub_council_area} - {self.hub_state}"

class EmailCollector(models.Model):
    class Meta:
        db_table = "Potential_Users_email"
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    date_added = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.email} - {self.date_added}"

class Transaction(models.Model):
    class Meta:
        db_table = "Transaction_table"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Coins Earned",default=0)
    transaction_type = models.TextField(max_length=500, verbose_name="Transaction Type", default="Credit")
    date_added_with_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.user} - {self.amount} - {self.transaction_type} - {self.date_added} - {self.date_added_with_time}"

class RecycledItems(models.Model):
    class Meta:
        db_table = "Recycled_Items_table"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_manufacturer = models.TextField(max_length=500, verbose_name="Item Manufacturer")
    item_barcode = models.TextField(max_length=500, verbose_name="Item Barcode")
    hub = models.TextField(max_length=200,verbose_name="Hub Name", default="WasteCoin Hub")
    hub_address = models.TextField(max_length=200,verbose_name="Address", default="Lugbe 1")
    hub_state = models.TextField(max_length=200,verbose_name="State", default="Abuja")
    hub_council_area = models.TextField(max_length=200,verbose_name="LGA/Council Area", default="AMAC")
    hub_country = models.TextField(max_length=200,verbose_name="Country",default="Nigeria" )
    date_added_with_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.user} - {self.item_manufacturer} - {self.item_barcode} - {self.hub} -{self.collected} -{self.paid} - {self.date_added}"

class Manufacturer(models.Model):
    class Meta:
        db_table = "Manufacturer_table"
    manufacturer = models.TextField(max_length=500, verbose_name="Item Manufacturer")
    barcode_identification = models.TextField(max_length=500, verbose_name="Item Barcode Identification")
    amount = models.FloatField(verbose_name="Coins Worth",default=0)
    date_added_with_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.manufacturer} - {self.barcode_identification} - {self.amount} - {self.date_added}"

class BrandCollector(models.Model):
    class Meta:
        db_table = "Brand_collector_table"
    brand = models.TextField(max_length=500, verbose_name="Item brand")
    barcode_identification = models.TextField(max_length=500, verbose_name="Item Barcode Identification")
    category = models.TextField(max_length=500, verbose_name="Category of Waste", default="Plastic")
    message = models.TextField(max_length=500, verbose_name="Feedback Message", default="hello admin!")
    date_added_with_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.brand} - {self.barcode_identification} - {self.category} - {self.message} - {self.date_added}"

class Notification(models.Model):
    class Meta:
        db_table = "Notification_table"
    sender = models.TextField(max_length=500, verbose_name="Sender Email", default="Admin")
    message = models.TextField(max_length=500, verbose_name="Message", default="hello admin!")
    ratings = models.TextField(max_length=500, verbose_name="Ratings", default="Excited")
    date_added_with_time = models.DateTimeField(default=timezone.now)
    date_added = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f"{self.sender} - {self.message} - {self.ratings} - {self.date_added}"