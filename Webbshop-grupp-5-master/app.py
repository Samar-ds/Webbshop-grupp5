from flask import Flask
from models import db, seedData, User, user_manager
from flask_migrate import Migrate, upgrade
from areas.site.sitePages import siteBluePrint
from areas.products.productPages import productBluePrint
from areas.admin.adminPages import AdminBluePrint
from areas.api.newsletterAPI_pages import apiNewsletterBluePrint
from areas.users.userPages import userBluePrint
from areas.cart.cartpages import CartBluePrint
from areas.wishlist.wishlistpages import wishlistBluePrint
from flask_user import current_user
from areas.cart.services import GetCurrentCartAmount, CartDropDown
from areas.wishlist.services import GetCurrentWishlistAmount

app = Flask(__name__)
app.config.from_object('config.ConfigDebug')
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

user_manager.app = app
user_manager.init_app(app,db,User)

app.register_blueprint(siteBluePrint)
app.register_blueprint(productBluePrint)
app.register_blueprint(AdminBluePrint)
app.register_blueprint(apiNewsletterBluePrint)
app.register_blueprint(userBluePrint)
app.register_blueprint(CartBluePrint)
app.register_blueprint(wishlistBluePrint)

@app.context_processor
def inject_cart_wishlist():
    if current_user.is_authenticated:
        amount = GetCurrentCartAmount(current_user)
        cartdropdown = CartDropDown(current_user)
        wishlistamount = GetCurrentWishlistAmount(current_user)
    else:
        amount = None
        cartdropdown = (None, None)
        wishlistamount = None
    return dict(amount=amount, cartdropdowntotal = cartdropdown[1], cartdropdownproducts=cartdropdown[0], wishlistamount=wishlistamount)

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()
