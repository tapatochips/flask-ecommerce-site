from app import app
from flask import render_template, flash, redirect, request, url_for
from .models import Inventory, User, Cart
from app.auth.forms import InventoryField
from flask_login import current_user



app.secret_key = 'my_secret_key'

@app.route('/')

@app.route('/index')
def base():
    cartSize = Cart.Size()
    products = Inventory.query.all()
    admin = User.is_admin()
    print(admin)
    return render_template('index.html', products=products, admin=admin, cartSize=cartSize)

@app.route('/cart')
def cart():
    cartSize = Cart.Size()

    usercart = Cart.query.filter_by(user_id=current_user.id).all()

    total = 0
    for cart in usercart:
        total += cart.item.price

    return render_template('cart.html', cartSize=cartSize, usercart=usercart, total=total)

@app.route('/addtocart/<int:prodid>')
def addToCart(prodid):
    item = Cart(current_user.id, prodid)
    item.saveToDB()
    flash('Item successfully added to your cart!', 'success')
    return redirect(url_for('base'))

@app.route('/removefromcart/<int:cartid>') #removes an item from the cart
def removeFromCart(cartid):
    removeme = Cart.query.filter_by(id=cartid).first()
    removeme.deleteFromDB()
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

@app.route('/emptycart')
def emptyCart():
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    for item in cart:
        item.deleteFromDB()
    flash('Purchase made successfully', 'success')
    return redirect(url_for('base'))

@app.route('/remove/<int:prodid>')
def removeItem(prodid): #This is an admin feature to remove an item from inventory
    deleteme = Inventory.query.filter_by(id=prodid).first()
    deleteme.deleteFromDB()
    return render_template('index.html')

@app.route('/edititem/<int:prodid>')
def editItem(prodid):
    item = Inventory.query.filter_by(id=prodid).first()
    if item:
        form = InventoryField()
        if request.method == 'POST':
            if form.validate():
                print('im right here')
                product_name = form.product_name.data
                price = form.price.data
                description = form.description.data
                image = form.image.data
                image2 = form.image2.data
                image3 = form.image3.data
                image4 = form.image4.data

                product = Inventory(product_name, price, description, image, image2, image3, image4)
                print('Product instance is created')
                product.saveToDB()
                flash('Product added to Inventory!', 'success')
                return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    cartSize = Cart.Size()
    product = Inventory.query.get_or_404(product_id)
    return render_template('product.html', product=product, cartSize=cartSize)


#flask run --port 8000
