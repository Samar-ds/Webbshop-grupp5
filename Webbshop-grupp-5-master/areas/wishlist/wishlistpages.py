from flask import Blueprint, redirect, render_template,request, url_for,flash
from flask_login import login_required
from .services import DeleteProductFromWishlist
from models import ProductWishlist, Wishlist, db, Product
from flask_user import current_user
from areas.cart.services import AddToCart

wishlistBluePrint = Blueprint('wishlist', __name__)


@wishlistBluePrint.route('/viewwishlist')
@login_required
def viewwishlist() -> str:
    wishlist = Wishlist.query.filter(Wishlist.UserID==current_user.id).first()
    total = 0
    products = {}
    deleteproduct = request.args.get("delete", default=False, type=bool)
    purchase = request.args.get("purchase", default=False, type=bool)
    if purchase == True:
        productid = request.args.get("productid", type=int)
        antal = request.args.get("antal", default=1, type=int)
        product = Product.query.filter(Product.ProductID==productid).first()
        if product.UnitsInStock < antal:
            flash("Sorry, this product is sold out at the moment")
            return redirect(url_for('wishlist.viewwishlist'))
        AddToCart(productid, current_user.id, antal)
        dell = ProductWishlist.query.filter(ProductWishlist.wishlist_id==wishlist.Id).filter(ProductWishlist.product_id==productid).first()
        db.session.delete(dell)
        db.session.commit()
        return redirect(url_for('wishlist.viewwishlist'))
    if deleteproduct == True:
        productid=request.args.get("productid", type=int)
        DeleteProductFromWishlist(productid, wishlist.Id)
        return redirect(url_for('wishlist.viewwishlist'))
    for p in wishlist.Products:
        amount = db.session.query(ProductWishlist.amount).filter(ProductWishlist.product_id==p.ProductID).first()
        products[p] = amount[0]
        total += (p.UnitPrice) * amount[0]
    return render_template('wishlist/viewwishlist.html', products=products, total="{:.2f}".format(total)) 