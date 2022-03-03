from flask import Blueprint, redirect, render_template,request, url_for, flash
from .services import getCategory, getTrendingCategories, getProduct, getTrendingProducts
from forms import CategoryForm, ProductForm, NewsletterForm
from models import db, Category, Product, Mails, ProductRating
from flask_user import roles_accepted, current_user
import random
from areas.cart.services import AddToCart
from areas.wishlist.services import AddToWishlist


productBluePrint = Blueprint('product', __name__)

@productBluePrint.route('/',methods=["GET","POST"])
def index() -> str:
    
    if current_user.is_authenticated:
        current = current_user._get_current_object()
        test = Mails.query.filter(Mails.Epostadress==current.email).filter(Mails.IsActive==1).first()
    else:
        test = None
    form = NewsletterForm(request.form)
    trendingCategories = []
    trendingCategories = getTrendingCategories()
    trendingProducts = getTrendingProducts()
    if form.validate_on_submit():
        if Mails.query.filter(Mails.Epostadress==form.EpostAdress.data).filter(Mails.IsActive==1).first():
            flash("Du är redan prenumerant")
            return render_template('products/index.html',trendingCategories=trendingCategories,
        products=trendingProducts,form=form, test=test
    )   
        mail = Mails.query.filter(Mails.Epostadress==form.EpostAdress.data).filter(Mails.IsActive==0).first()
        if mail:
            mail.IsActive = True
            db.session.commit()
            flash("Välkommen tillbaka!")
            test = mail
            return render_template('products/index.html',trendingCategories=trendingCategories,
        products=trendingProducts,form=form, test=test
    )
        mail = Mails()
        mail.Epostadress = form.EpostAdress.data
        mail.IsActive = True
        db.session.add(mail)
        db.session.commit()
        flash("Tack!")
    
    return render_template('products/index.html',trendingCategories=trendingCategories,
        products=trendingProducts,form=form, test=test
    )
@productBluePrint.route('/category/<id>')
def category(id) -> str:
    category = getCategory(id)
    purchase = request.args.get("purchase", default=False, type=bool)
    wishlist = request.args.get("wishlist", default=False, type=bool)
    if wishlist == True:
        productid = request.args.get("productid", type=int)
        product = Product.query.filter(Product.ProductID==productid).first()
        AddToWishlist(productid, current_user.id)
        return redirect(url_for('product.category', id=category.CategoryID))
    if purchase == True:
        productid = request.args.get("productid", type=int)
        product = Product.query.filter(Product.ProductID==productid).first()
        if product.UnitsInStock <= 0:
            flash("Sorry, this product is sold out at the moment")
            return redirect(url_for('product.category', id=category.CategoryID))
        AddToCart(productid, current_user.id, 1)
        return redirect(url_for('product.category', id=category.CategoryID))
    return render_template('products/category.html',category=category)

@productBluePrint.route('/product/<id>',methods=['GET','POST'])
def product(id) -> str:
    product = getProduct(id)

    ratingstore = ProductRating.query.filter(ProductRating.Product_id==id).first()

    # if request.method == 'POST':
    five_stars = ratingstore.Point_5
    four_stars = ratingstore.Point_4
    three_stars = ratingstore.Point_3
    two_stars = ratingstore.Point_2
    one_star = ratingstore.Point_1
    count = ratingstore.Point_count
    rating = ratingstore.Point_avarage
    total = ratingstore.Point_total
    # if request.method == 'POST':
    if 'rating' in request.form:
        content = int(request.form['rating'])
        if content:
            if content == 5:
                five_stars += 1
            elif content == 4:
                four_stars += 1
            elif content == 3:
                three_stars += 1
            elif content == 2:
                two_stars += 1                    
            elif content == 1:
                one_star += 1
            count += 1
            total += content
            rating = float('{0:.1f}'.format(total/count))
    ratingstore.Point_5 = five_stars
    ratingstore.Point_4 = four_stars
    ratingstore.Point_3 = three_stars
    ratingstore.Point_2 = two_stars
    ratingstore.Point_1 = one_star
    ratingstore.Point_count = count
    ratingstore.Point_avarage = rating
    ratingstore.Point_total = total
        
    product.Rating = ratingstore.Point_avarage
    db.session.commit()
    return render_template('products/product.html',product=product, five_stars=five_stars, four_stars=four_stars, three_stars=three_stars, two_stars=two_stars, one_star=one_star, count=count, rating=rating)

@productBluePrint.route('/addcategory', methods=["GET", "POST"])
@roles_accepted("Admin")
def addCategory() -> str:
    form = CategoryForm(request.form)
    if Category.query.filter(Category.CategoryName==form.CategoryName.data).first():
        flash(f"Category already exist")
        return render_template('products/addCategory.html', form=form)
    if form.validate_on_submit():
        newCat = Category()
        newCat.CategoryName = form.CategoryName.data
        newCat.Description = form.Description.data
        db.session.add(newCat)
        db.session.commit()
        return redirect(url_for('product.index'))
    return render_template('products/addCategory.html', form=form)

@productBluePrint.route('/allcategories')
@roles_accepted("Admin")
def allcategories() -> str:
    Categories = Category.query.all()
    return render_template('products/allcategories.html', Categories=Categories)

@productBluePrint.route('/editcategory/<id>', methods=["GET", "POST"])
@roles_accepted("Admin")
def editcategory(id) -> str:
    category = Category.query.filter(Category.CategoryID==id).first()
    form = CategoryForm(request.form)
    if request.method == "GET":
        form.CategoryName.data = category.CategoryName
        form.Description.data = category.Description
    if form.validate_on_submit():
        if form.CategoryName.data != category.CategoryName and Category.query.filter(Category.CategoryName==form.CategoryName.data).first() != None:
            flash(f"Category already exist")
            return render_template('products/editCategory.html', category=category, form=form)
        category.CategoryName = form.CategoryName.data
        category.Description = form.Description.data
        db.session.commit()
        return redirect(url_for('product.index'))
    return render_template('products/editCategory.html', category=category, form=form)

@productBluePrint.route('/addproduct', methods=["GET", "POST"])
@roles_accepted("Admin")
def addProduct() -> str:
    form = ProductForm(request.form)
    categorychoices = []
    for cat in Category.query.all():
        categorychoices.append((cat.CategoryID, cat.CategoryName))
    form.CategoryId.choices = categorychoices
    if Product.query.filter(Product.ProductName==form.ProductName.data).first():
        flash(f"Product already exist")
        return render_template('products/addProduct.html', form=form)
    form.Discontinued.data = True
    if form.validate_on_submit():
        newprod = Product()
        newprod.ProductName = form.ProductName.data
        newprod.SupplierID = random.randint(1, 29)
        newprod.CategoryId = form.CategoryId.data
        newprod.QuantityPerUnit = form.QuantityPerUnit.data
        newprod.UnitPrice = form.UnitPrice.data
        newprod.UnitsInStock = form.UnitsInStock.data
        newprod.UnitsOnOrder = 0
        newprod.ReorderLevel = form.ReorderLevel.data
        newprod.Discontinued = False
        newprod.Rating = 0
        newprod.CampaignPrice = form.CampaignPrice.data
        db.session.add(newprod)
        db.session.commit()

        newprod = Product.query.filter_by(ProductName=form.ProductName.data).first()
        new = ProductRating()
        new.Product_id = newprod.ProductID
        new.Point_1 = 0 
        new.Point_2 = 0
        new.Point_3 = 0
        new.Point_4 = 0
        new.Point_5 = 0
        new.Point_avarage = 0
        new.Point_total = 0
        new.Point_count = 0
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('product.index'))
    return render_template('products/addProduct.html', form=form)

@productBluePrint.route('/allproducts')
@roles_accepted("Admin")
def allproducts() -> str:
    Products = db.session.query(Product, Category.CategoryName).join(Category).all()
    return render_template('products/allproducts.html', Products=Products)

@productBluePrint.route('/editproduct/<id>', methods=["GET", "POST"])
@roles_accepted("Admin")
def editproduct(id) -> str:
    product = Product.query.filter(Product.ProductID==id).first()
    form = ProductForm(request.form)
    categorychoices = []
    for cat in Category.query.all():
        categorychoices.append((cat.CategoryID, cat.CategoryName))
    form.CategoryId.choices = categorychoices
    if request.method == "GET":
        form.ProductName.data = product.ProductName
        form.CategoryId.data = product.CategoryId
        form.QuantityPerUnit.data = product.QuantityPerUnit
        form.UnitPrice.data = product.UnitPrice
        form.UnitsInStock.data = product.UnitsInStock
        form.ReorderLevel.data = product.ReorderLevel
        form.Discontinued.data = product.Discontinued
        form.CampaignPrice.data = product.CampaignPrice
    if form.validate_on_submit():
        if form.ProductName.data != product.ProductName and Product.query.filter(Product.ProductName==form.ProductName.data).first() != None:
            flash(f"Product already exist")
            return render_template('products/editProduct.html', product=product, form=form)
        product.ProductName = form.ProductName.data
        product.CategoryId = form.CategoryId.data
        product.QuantityPerUnit = form.QuantityPerUnit.data
        product.UnitPrice = form.UnitPrice.data
        product.UnitsInStock = form.UnitsInStock.data
        product.ReorderLevel =  form.ReorderLevel.data
        product.Discontinued = form.Discontinued.data
        product.CampaignPrice = form.CampaignPrice.data
        db.session.commit()
        return redirect(url_for('product.index'))
    return render_template('products/editProduct.html', product=product, form=form)



