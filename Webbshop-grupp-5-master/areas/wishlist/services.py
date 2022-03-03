from models import Product, ProductCart, Cart, ProductWishlist, Wishlist, db
from sqlalchemy.sql import functions

def AddToWishlist(productId, UserId):
    wishlist = Wishlist.query.filter(Wishlist.UserID==UserId).first()
    exist = ProductWishlist.query.filter(ProductWishlist.wishlist_id==wishlist.Id).filter(ProductWishlist.product_id==productId).first()
    if exist:
        exist.amount += 1
        db.session.commit()
        return
    new = ProductWishlist()
    new.product_id = productId
    new.wishlist_id = wishlist.Id
    new.amount = 1
    db.session.add(new)
    db.session.commit()

def GetCurrentWishlistAmount(current_user):
    wishlist = Wishlist.query.filter(Wishlist.UserID==current_user.id).first()
    amount = db.session.query(functions.sum(ProductWishlist.amount)).filter(ProductWishlist.wishlist_id==wishlist.Id).scalar()
    if amount == None:
        amount = 0
    return amount

def DeleteProductFromWishlist(productid, wishlistid):
    delete = ProductWishlist.query.filter(ProductWishlist.product_id==productid).filter(ProductWishlist.wishlist_id==wishlistid).first()
    db.session.delete(delete)
    db.session.commit()
