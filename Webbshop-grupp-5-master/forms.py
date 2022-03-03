from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField
from wtforms.fields import IntegerField, FloatField, BooleanField, RadioField
from flask_user.forms import RegisterForm
from models import User

class NewsletterForm(FlaskForm):
    EpostAdress = StringField("Enter Your Email", [validators.Email()])
    

class CategoryForm(FlaskForm):
    CategoryName = StringField("Category name", [validators.Length(min=3,max=80)])
    Description = TextAreaField("Description", [validators.Length(min=3,max=80)])

class ProductForm(FlaskForm):
    ProductName = StringField("Product name", [validators.Length(min=3,max=40)])
    CategoryId = SelectField(u"Category", coerce=int)
    QuantityPerUnit = StringField("Quantity per unit", [validators.Length(min=3,max=20)])
    UnitPrice = FloatField("Unit price", [validators.NumberRange(min=0)])
    UnitsInStock = IntegerField("Units in stock", [validators.NumberRange(min=0)])
    ReorderLevel = IntegerField("Reorder level", [validators.NumberRange(min=0)])
    Discontinued = BooleanField("Discontinued", render_kw={'style':'width:8%'})
    CampaignPrice = IntegerField("Campaign price", [validators.NumberRange(min=0, max=100)])

class AddNewsletterForm(FlaskForm):
    Title = StringField("Title", [validators.Length(min=3,max=40)])
    Content = TextAreaField("Content", [validators.Length(min=3,max=1000)])

class EditUser(FlaskForm):
    first_name = StringField("Firstname", [validators.Length(min=3,max=100)])
    last_name = StringField("Lastname", [validators.Length(min=3,max=100)])

class DeleteUser(FlaskForm):
    Answer = RadioField("Are you sure?", choices=[('y', 'Yes'), ('n','No')], render_kw={'style':'list-style:none; border:0;'})

class CheckoutForm(FlaskForm):
    Cardnumber = IntegerField("Cardnumber", [validators.NumberRange(min=1000000000000000, max=9999999999999999)])
    CVC = IntegerField("CVC", [validators.NumberRange(min=100, max=999)])

class NewUserForm(RegisterForm):
    first_name = StringField("Firstname", [validators.Length(min=3,max=100)])
    last_name = StringField("Lastname", [validators.Length(min=3,max=100)])

    class Meta:
        model = User
        fields = ["first_name","last_name","email", "password", "retype_password", "submit"]
