from flask import Blueprint, flash, redirect, render_template, request, url_for
from .forms import LogIn, SignUpForm
from ..models import User
from flask_login import current_user, login_user, logout_user, login_required, login_manager

auth = Blueprint('auth', __name__, template_folder='auth_templates')



@auth.route('/signup', methods = ["GET", "POST"])
def signup():
    
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            
            
            user = User(first_name, last_name, email, username, password)
            
            user.save_to_db()
            account = {
                'email': email,
                'username': username
            }
        flash('Signed up successfully!', "success")
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form = form)


@auth.route('/signin', methods = ["GET", "POST"])
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
                if user.password == password:
                    login_user(user)
                    flash('Signed in successfully', "success")
                    return redirect(url_for('base'))
                else:
                    flash('invalid username or password', "danger")
            else:
                flash('Invalid username or password', "danger")
                
    return render_template('signin.html', form = form)

#auth
@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('auth.signin'))

@auth.route('/admin')
def adminDash():
    if User.is_admin():
        return render_template('admin.html')
    else:
        return redirect(url_for('base'))



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