from . import api
from ..models import *
from ..api_auth_helper import token_auth
from flask import request, redirect
from flask_login import current_user
import os
import stripe

stripe.api_key = os.environ.get('STRIPE_API_KEY')



@api.get('/products')
def getProductsAPI(): 
    products = Inventory.query.all()
    return {
        'status':'ok',
        'results': len(products),
        'products': [p.to_dict() for p in products]
    }

@api.get('/cart')
@token_auth.login_required
def getCartAPI():
    user = token_auth.current_user()
    return {
        'status': 'ok',
        'cart': [Inventory.query.get(c.prod_id).to_dict() for c in Cart.query.filter_by(user_id=user.id).all()]
    }
    
@api.post('/cart')
@token_auth.login_required
def addToCartAPI():
    user = token_auth.current_user()
    data = request.json

    product_id = data['id']
    product = Inventory.query.get(product_id)

    if product:

        cart_item = Cart(user.id, product.id)
        cart_item.saveToDB()

        return {
            'status': 'ok',
            'message': f'Succesfully added {product.product_name} to your cart!'
        }
    else:
        return {
            'status': 'not ok',
            'message': 'That product does not exist!'
        }
    
@api.delete('/cart/<int:product_id>')
@token_auth.login_required
def removeFromCartAPI(product_id):
    user = token_auth.current_user()
    product = Inventory.query.get(product_id)
    item = Cart.query.filter_by(user_id=user.id).filter_by(prod_id=product_id).first()
    if item:
        item.deleteFromDB()
        return {
            'status': 'ok',
            'message': f"Successfully removed {product.product_name} from cart."
        }
    return {
            'status': 'not ok',
            'message': f"You do not have that item in your cart."
        }

@api.post("/create-checkout-session")
def checkout():
    
    try:
        data = request.form
        print(data.items)
        user = data.get('user')
        print(user)
        line_items = []
        for price, qty in data.items():
            line_items.append({
                'price':price,
                'quantity':qty
            }),
        checkout_session = stripe.checkout.Session.create(
            customer_email = user['email'],
        billing_address_collection='auto',
        shipping_address_collection={
            "allowed_countries":['US','CA']
        },
            line_items=line_items,
            mode='payment',
            success_url ='FRONT_END_URL'+'?success=true',
            cancel_url ='FRONT_END_URL'+'?canceled=true',
        )
        
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)
        
