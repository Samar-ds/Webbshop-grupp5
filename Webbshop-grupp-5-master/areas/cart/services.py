from models import Product, ProductCart, Cart, db
from sqlalchemy.sql import functions

def AddToCart(productId, UserId, amount):
    cart = Cart.query.filter(Cart.UserID==UserId).first()
    exist = ProductCart.query.filter(ProductCart.cart_id==cart.Id).filter(ProductCart.product_id==productId).first()
    product = Product.query.filter(Product.ProductID==productId).first()
    product.UnitsInStock -= amount
    if exist:
        exist.amount += amount
        db.session.commit()
        return
    new = ProductCart()
    new.product_id = productId
    new.cart_id = cart.Id
    new.amount = amount
    db.session.add(new)
    db.session.commit()

def GetCurrentCartAmount(current_user):
    cart = Cart.query.filter(Cart.UserID==current_user.id).first()
    amount = db.session.query(functions.sum(ProductCart.amount)).filter(ProductCart.cart_id==cart.Id).scalar()
    if amount == None:
        amount = 0
    return amount

def DeleteProductFromCart(productid, cartid):
    delete = ProductCart.query.filter(ProductCart.product_id==productid).filter(ProductCart.cart_id==cartid).first()
    product = Product.query.filter(Product.ProductID==productid).first()
    product.UnitsInStock += delete.amount
    db.session.delete(delete)
    db.session.commit()


def CartDropDown(current_user):
    cart = Cart.query.filter(Cart.UserID==current_user.id).first()
    products = {}
    total = 0
    for p in cart.Products:
        amount = db.session.query(ProductCart.amount).filter(ProductCart.product_id==p.ProductID).first()
        products[p] = amount[0]
        total += (p.UnitPrice) * amount[0]
    return products, total