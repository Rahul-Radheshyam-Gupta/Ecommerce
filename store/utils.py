import json
from store.models import Product

def get_cart_cookies(request):
    cookies = json.loads(request.COOKIES.get('cart'))
    order = {}
    items = []
    # if cookies:
    #     order["get_cart_total"] = cookies
    get_cart_total = 0
    get_total_items = 0
    shipping = True
    print("cookies ",cookies)
    for product_id in cookies:
        # try except to handle error if admin delete some product and we still have product id in cookie
        try:
            item = {}
            product = Product.objects.get(id=product_id)
            get_total_items += cookies[product_id]["quantity"]
            get_cart_total += product.price * cookies[product_id]["quantity"]
            item["quantity"] = cookies[product_id]["quantity"]
            item["product"] = product
            items.append(item)
            if product.digital:
                shipping = False
        except:
            print("product is deleted by admin ",product_id)
    return items,get_total_items,get_cart_total,shipping
        