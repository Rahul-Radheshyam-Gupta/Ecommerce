var updatebtns = document.getElementsByClassName('update-cart')

for(var i =0;i<updatebtns.length;i++){
    updatebtns[i].addEventListener('click',function(){
        var product = this.dataset.product // product id
        var action = this.dataset.action // add or remove action
        console.log(product,action) 
        if(user=="AnonymousUser"){
            console.log("AnonymousUser")
            updateCookieItem(product,action);        
        }
        else{
            updateUserOrder(product,action)
        }
    })
}

// update cooki function called for Anonymous user
function updateCookieItem(product, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[product] == undefined){
		cart[product] = {'quantity':1}

		}else{
			cart[product]['quantity'] += 1;
		}
	}

	if (action == 'remove'){
		cart[product]['quantity'] -= 1;
		if (cart[product]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[product];
		}
	}
    console.log('CART:', cart);
    // json to string before adding in cookie
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload()
    // var cart_list = JSON.parse(getCookie("cart"));
    // console.log("list of cart ",cart_list)
    // var total_items = 0;
    // for(var key in cart_list){
    //     if(cart_list.hasOwnProperty(key))
    //         total_items += cart_list[key]["quantity"]
    // }
    // if(total_items>0){
    //     console.log("total items",total_items)
    //     $('.cart_total').text(total_items)
    // }
}





function updateUserOrder(product,action){
    // pls see url pattern -- 
    $.ajax({
        url:"/update_item/",
        type:'POST',
        data:{
            'product':product,
            'action':action,
            'csrfmiddlewaretoken':csrfmiddlewaretoken
              },
        dataType: 'json',
        success:function(data){

            console.log(data)
            $('.cart').text(data.get_total_items)
            
            if(String(data.get_cart_total).indexOf(".")!=-1){
                $('.cart_total').text(data.get_cart_total)
            }
            else{
                $('.cart_total').text(data.get_cart_total+".00")
            }
            var price_id = "#price_"+product;
            var quantity_id = "#quantity_"+product;
            console.log("====================",price_id,quantity_id)
            if($(price_id).text()){
            var price = parseFloat($(price_id).text());
            var quantity = parseInt($(quantity_id).text());
            }
            else{
                var price = false;
                var quantity = false;
            }
            console.log("====================",typeof(price))
            
            if (price && quantity){
                var total_id = "#total_"+product;
                console.log(price,quantity,total_id)
                console.log("=== total ",$(total_id).html())
                if(action == "add"){
                        quantity = parseInt(quantity)+1;
                        var sum = price*quantity;
                        if(String(sum).indexOf(".")!=-1){
                            $(total_id).text(sum);
                        }
                        else{
                            $(total_id).text(sum+".00");
                        }

                        $(quantity_id).text(quantity);
                }
                else if(action == "remove"){
                    quantity = parseInt(quantity)-1
                    if(quantity>0){
                        var sum = price*quantity;
                        if(String(sum).indexOf(".")!=-1){
                            $(total_id).text(sum);
                        }
                        else{
                            $(total_id).text(sum+".00");
                        }
                        $(quantity_id).text(quantity);
                    }
                    else{
                        $(total_id).parent().parent().hide();
                    }
                }
            }
        }
    })
}





