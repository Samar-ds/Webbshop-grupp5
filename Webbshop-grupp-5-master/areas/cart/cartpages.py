from flask import Blueprint, redirect, render_template,request, url_for
from flask_login import login_required
from .services import DeleteProductFromCart
from forms import CheckoutForm
from models import db,ProductCart, Cart
from flask_user import current_user

CartBluePrint = Blueprint('cart', __name__)


@CartBluePrint.route('/viewcart')
@login_required
def viewcart() -> str:
    cart = Cart.query.filter(Cart.UserID==current_user.id).first()
    total = 0
    products = {}
    deleteproduct = request.args.get("delete", default=False, type=bool)
    if deleteproduct == True:
        productid=request.args.get("productid", type=int)
        DeleteProductFromCart(productid, cart.Id)
        return redirect(url_for('cart.viewcart'))
    for p in cart.Products:
        amount = db.session.query(ProductCart.amount).filter(ProductCart.product_id==p.ProductID).first()
        products[p] = amount[0]
        total += (p.UnitPrice) * amount[0]
    return render_template('cart/viewcart.html', products=products, total="{:.2f}".format(total)) 

@CartBluePrint.route('/thanksforpurchase')
@login_required
def thanksforpurchase():
    return render_template('/cart/thanksforpurchase.html')


@CartBluePrint.route('/Checkout', methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        cart = Cart.query.filter(Cart.UserID==current_user.id).first()
        for prod in ProductCart.query.filter(ProductCart.cart_id==cart.Id).all():
            db.session.delete(prod)
        db.session.commit()
        return redirect(url_for('cart.thanksforpurchase'))
    return render_template('/cart/checkout.html', form=form)

