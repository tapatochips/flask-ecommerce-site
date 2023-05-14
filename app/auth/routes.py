from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import Address, LogIn, SignUpForm, InventoryField
from ..models import Cart, Inventory, Order, User
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods=["GET", "POST"])
def signup():

    form = SignUpForm()

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data

            user = User(username, password, first_name, last_name, email)

            user.saveToDB()
            flash('Signed up successfully!', "success")
            return redirect(url_for('auth.signin'))
    return render_template('signup.html', form=form)


@auth.route('/signin', methods=["GET", "POST"])
def signin():
    form = LogIn()
    if request.method == 'POST':
        if form.validate():
            print('im here')
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            print(user, 'befor if statement')
            if user:
                print(user, 'inside if statement')
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Signed in successfully', "success")
                    return redirect(url_for('site.base'))
                else:
                    flash('invalid username or password', "danger")
            else:
                flash('Invalid username or password', "danger")

    return render_template('signin.html', form=form)

# auth


@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    flash("You've been successfully logged out", 'success')
    return redirect(url_for('auth.signin'))

@auth.route('/admin', methods=["GET", "POST"])
@login_required
def adminDash():
    print('in the route')
    form = InventoryField()
    user = current_user
    if user.is_admin():
        print('The user is an admin!!')
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

                return render_template('admin.html', form=form)
    return render_template('admin.html', form=form)


@auth.route('/user')
@login_required
def user():

    return render_template('base.html', user=current_user)


# @auth.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if request.method == "POST" and form.validate_on_submit():
#         print('here')
#         edited_user_data = {
#         'email':form.email.data,
#         'username':form.username.data,
#         'password':form.password.data,
#         }
#         user = User.query.filter_by(email = edited_user_data['email']).first()
#         if user and user.email != current_user.email:
#             flash('email is already in use', "danger")
#             return redirect(url_for('auth.edit_profile'))
#         try:
#             current_user.from_dict(edited_user_data)
#             current_user.save_to_db()
#             flash('profile updated', "success")

#         except:
#             flash('error updating profile', 'danger')
#             return redirect(url_for('auth.edit_profile'))
#         return redirect(url_for('auth.user'))
#     return render_template('edit_profile.html', form = form)
