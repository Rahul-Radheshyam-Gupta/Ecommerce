from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum,Count
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# rahul - rahul
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True,blank=True)
	email = models.CharField(max_length=200)
	is_vendor = models.BooleanField(default=False) # new 
	def __str__(self):
		return self.name


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        check_customer = Customer.objects.filter(email=instance.email)
        if check_customer:
            customer = check_customer.first()
            customer.user = instance
            customer.name = instance.username
            customer.save()
        else:
            Customer.objects.create(user=instance,email=instance.email,name=instance.username)

    instance.customer.save()

class Product(models.Model):
	added_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="products") #new
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False)
	image = models.ImageField(null=True,blank=True)
	description = models.TextField(max_length=1000,null=True,blank=True)
	is_active = models.BooleanField(default=True)
    

	def __str__(self):
		return self.name
	
	@property
	def get_image_url(self):
		try:
			return self.image.url
		except :
			return ''

	@property
	def get_total_item_sell(self):
		try:
			items = self.orderitem_set.values_list('quantity',flat=True)
			return sum(items)
		except :
			return 0

# consider it as cart --- as cart table
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)


	def __str__(self):
		return str(self.id)


	@property
	def get_cart_total(self):
		return sum([ 
			item.quantity*item.product.price for item in self.orderitem_set.all()
			])
	
	@property
	def get_total_items(self):
		return sum([
			item.quantity for item in self.orderitem_set.all()
		])

	@property
	def shipping(self):
		items = self.orderitem_set.all()
		x = items.values_list('product__digital',flat=True)
		if True in x:
			return False
		return True


# considerit as a row of cart table
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address