from django.shortcuts import render,redirect,reverse
from .models import *
import  json
# Create your views here.
from django.http import  JsonResponse
from datetime import  datetime
import uuid
from store.utils import get_cart_cookies
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
def log_out(request):
	logout(request)
	request.session['authenticated'] = False
	return render(request,'store/login.html')

def registeration(request):
	error = {}
	if request.method == "POST":
		print("request ",request.POST)
		username = request.POST.get('username')
		email = request.POST.get('email')
		psw1 = request.POST.get('password1')
		psw2 = request.POST.get('password2')
		# validation
		if not (username and email and psw1 and psw2):
			error['error'] = 'Please fill all fields'
		if psw1 != psw2:
			error['error'] = 'Password mismatch'
		if len(psw1) < 8:
			error['error'] = 'Password length must be equal or greater than 8'
		check_user = User.objects.filter(email=email).first()
		if check_user:
			error['error'] = f'Email {email} is already registered with us'

		# end of validation
		# check if any error then redirect to sign up page with error
		# else create user and do authentication and redirect to dashboard
		if error:    
			messages.warning(request, error['error'])
			request.session['authenticated'] = False
			return render(request,'store/registration.html',error)
		else:
			new_user = User.objects.create_user(username,email,psw1)
			new_user.save()

			#do authentication
			user = authenticate(request,username=username,password=psw1)
			print('user ',user)
			# after signup direct run login 
			login(request,user)
			request.session['authenticated'] = True
			messages.success(request, 'Successfully account created')
			return HttpResponseRedirect(reverse('store'))
	return render(request,'store/registration.html',error)

def store_login(request):
	error = {}
	if request.method == "POST":
		print(request.POST)
		email = request.POST.get('email')
		psw = request.POST.get('password')
		# validation
		if not (email and psw):
			error['error'] = 'Please fill all fields'

		get_user_obj = User.objects.filter(email=email)
		if not get_user_obj:
			error['error'] = f'No account with {email}'
		
		if error:
			request.session['authenticated'] = False
			messages.warning(request, error['error'])
			return render(request,'store/login.html',error)
		else:
			user = get_user_obj.first()
			login(request,user)
			request.session['authenticated'] = True
			messages.success(request, 'Successfully login')
			return HttpResponseRedirect(reverse('store'))
	return render(request,'store/login.html',error)

def store(request):
	context = {}
	template_name = 'store/store.html'
	products = Product.objects.all()
	context["products"] = products
	if request.user.is_authenticated:
		customer = request.user.customer
		print("count",Order.objects.filter(customer=customer,complete=False))
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
	else:
		order = {}
		cookies = json.loads(request.COOKIES.get('cart'))
		get_total_items = 0   
		if cookies:    
			for product_id in cookies:
				get_total_items += cookies[product_id]["quantity"]
		order["get_total_items"] = get_total_items
	context['order'] = order
	return render(request,template_name, context)


def cart(request):
	context = {}
	template_name = 'store/cart.html'

	# true if user is logged in
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=0)
		# list of items in the order cart has
		items = order.orderitem_set.all()
	else:
		order = {}
		data = get_cart_cookies(request)
		items = data[0]
		order["get_total_items"] = data[1]
		order["get_cart_total"] = data[2]
		order["shipping"] = data[3]

	context['items'] = items
	context['order'] = order
	return render(request,template_name, context)

def checkout(request):
	context = {}
	if request.method == 'POST':
		if request.is_ajax():
			transaction_id = uuid.uuid4()
			user_data = json.loads(request.POST['user_data'])
			shipping_data = json.loads(request.POST['shipping_data'])
			if request.user.is_authenticated:
				customer = request.user.customer
				order,created = Order.objects.get_or_create(customer=customer,complete=0)                
			else:
				name = user_data.get("name")
				email = user_data.get("email")
				if email:
					customer,created = Customer.objects.get_or_create(email=email)
					customer.name = name
					customer.save()
					order = Order.objects.create(customer=customer,complete=False)
					data = get_cart_cookies(request)
					if data:
						items = data[0]
						for item in items:
							order_item = OrderItem.objects.create(product=item["product"],order=order,quantity=item["quantity"])
				else:
					return JsonResponse({'message':"Please fill all details correctly."})

				print("unauthenticated")
			
			submitted_total = float(user_data["total"])
			print("submitted total ",submitted_total,order.get_cart_total)
			order.transaction_id = transaction_id
			if submitted_total == order.get_cart_total:
				print("order true")
				order.complete = True
				order.save()


			if order.shipping:
				shipping_obj = ShippingAddress.objects.create(
					customer = customer,
					order = order,
					city = shipping_data.get("city"),
					state = shipping_data.get("state"),
					zipcode = shipping_data.get("zipcode"),
					address = shipping_data.get("address")
				)
				print("process_Daa",user_data,shipping_data)

			return JsonResponse({'message':"Successful"})

	template_name = 'store/checkout.html'
	# true if user is logged in
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=0)
		# list of items in the order cart has
		items = order.orderitem_set.all()
	else:
		order = {}
		data = get_cart_cookies(request)
		items = data[0]
		order["get_total_items"] = data[1]
		order["get_cart_total"] = data[2]
		order["shipping"] = data[3]
	print("=== order ",order)
	context['items'] = items
	context['order'] = order
	return render(request,template_name, context)

def updateItem(request):
	print("process data ",request.POST)
	if request.method == 'POST':
		
		if request.is_ajax():
			product_id = request.POST.get('product',None)
			action = request.POST.get('action',None)

			# order associated with the user
			# user add item first time in cart the order will be created
			# else we will ask for order (not completed) already associated with user
			order,created = Order.objects.get_or_create(customer=request.user.customer,complete=False)

			# then we need to update product in order list
			# Order and Product are linked through the OrderItem
			# Order will have list of item (products)
			# item (order item) which represent product and in its quantity in the user's order
			product = Product.objects.get(id=product_id)

			order_item,created = OrderItem.objects.get_or_create(product = product,order=order) 
			if action == "add":
				order_item.quantity += 1
			elif action == "remove":
				order_item.quantity -= 1
			order_item.save()
			print(vars(order_item))
			
			# quantity of order item is 0 then delete the item from order
			# note we order item not product directly coz we dont want to delete a product
			if order_item.quantity <=0:
				order_item.delete()
			return JsonResponse({'message':"Successful","get_total_items":order.get_total_items,"get_cart_total":order.get_cart_total})
	return JsonResponse("Item added",safe=False)


