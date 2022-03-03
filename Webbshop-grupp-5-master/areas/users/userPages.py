from flask import Blueprint, redirect, render_template, request, url_for, flash, current_app
import flask_login
from flask_user import current_user
from forms import EditUser, DeleteUser, NewUserForm
from models import UserRoles, Wishlist, db, User, Cart
from flask_user.password_manager import PasswordManager
from flask_user.email_manager import EmailManager


userBluePrint = Blueprint('users', __name__)

@userBluePrint.route('/myaccount')
def MyAccount():
    user = current_user._get_current_object()
    return render_template('users/myaccount.html', user=user)

@userBluePrint.route('/edituser', methods=["GET", "POST"])
def EditUsers():
    user = current_user._get_current_object()
    form = EditUser(request.form)
    if request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('users.MyAccount'))
    return render_template('users/edituser.html', form=form)


@userBluePrint.route('/deleteuser', methods=["GET", "POST"])
def DeleteUsers():
    user = current_user._get_current_object()
    form = DeleteUser(request.form)

    if form.validate_on_submit():
        if form.Answer.data == "y":
            flask_login.logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('product.index'))
        else:
            return redirect(url_for('users.MyAccount'))
    return render_template('users/deleteuser.html', form=form)

@userBluePrint.route('/newuser', methods=["GET", "POST"])
def NewUser():
    form = NewUserForm(request.form)

    exist = User.query.filter(User.email==form.email.data).first()
    if exist:
        flash(f"The user already exist")
        return render_template('users/newuser.html', form=form)
    if form.password.data != form.retype_password.data:
        flash(f"Password does not match")
        return render_template('users/newuser.html', form=form)
   
    if form.validate_on_submit():
        Adduser = User()
        Adduser.email = form.email.data
        Adduser.first_name = form.first_name.data
        Adduser.last_name = form.last_name.data
        password_manager = PasswordManager(current_app)
        email_manager = EmailManager(current_app)
        Adduser.password = password_manager.hash_password(form.password.data)  
        db.session.add(Adduser)
        
        user = User.query.filter(User.email==form.email.data).first()

        role = UserRoles()
        role.role_id = 2
        role.user_id = user.id
        

        cart = Cart()
        cart.UserID = user.id

        whishlist = Wishlist()
        whishlist.UserID = user.id

        db.session.add(role)
        db.session.add(cart)
        db.session.add(whishlist)

        db.session.commit()
        email_manager.send_confirm_email_email(Adduser, Adduser)
        return redirect(url_for('user.login', id=Adduser.id))
    return render_template('users/newuser.html', form=form)


