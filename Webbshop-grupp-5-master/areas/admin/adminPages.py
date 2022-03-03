from flask import Blueprint, redirect, render_template,request, url_for
from flask_user import roles_accepted
from flask_mail import Message, Mail
from forms import AddNewsletterForm
from models import Mails, Newsletter, db, NewsletterMails

AdminBluePrint = Blueprint('Admin', __name__)

@AdminBluePrint.route('/addnewsletter', methods=["GET", "POST"])
@roles_accepted("Admin")
def addNewletter() -> str:
    form = AddNewsletterForm(request.form)
    if form.validate_on_submit():
        newsletter = Newsletter()
        newsletter.Title = form.Title.data
        newsletter.Content = form.Content.data
        newsletter.HasBeenSent = False
        db.session.add(newsletter)
        db.session.commit()
        return redirect(url_for('Admin.allnewsletters'))
    return render_template('admin/addNewsletter.html', form=form)

@AdminBluePrint.route('/allnewsletters')
@roles_accepted("Admin")
def allnewsletters() -> str:
    sortOrder = request.args.get('sortOrder', '0')

    if sortOrder == "" or sortOrder == None:
        sortOrder = "0"

    if sortOrder == "0":
        newsletters = Newsletter.query.filter(Newsletter.HasBeenSent == 0).all()
    if sortOrder == "1":
        newsletters = Newsletter.query.filter(Newsletter.HasBeenSent == 1).all()
    return render_template('admin/allnewsletters.html', newsletters=newsletters , sortOrder=sortOrder)


@AdminBluePrint.route('/editnewsletter/<id>', methods=["GET", "POST"])
@roles_accepted("Admin")
def editnewsletter(id) -> str:
    newsletter = Newsletter.query.filter(Newsletter.NewsletterId==id).first()
    form = AddNewsletterForm(request.form)
    if request.method == "GET":
        form.Title.data = newsletter.Title
        form.Content.data = newsletter.Content
    if form.validate_on_submit():
        newsletter.Title = form.Title.data
        newsletter.Content = form.Content.data
        db.session.commit()
        return redirect(url_for('Admin.allnewsletters'))
    return render_template('admin/editnewsletter.html', newsletter=newsletter, form=form)


@AdminBluePrint.route('/viewnewsletter/<id>')
@roles_accepted("Admin")
def viewnewsletters(id) -> str:
    newsletter = Newsletter.query.filter(Newsletter.NewsletterId==id).first()
    mails = db.session.query(Mails.Epostadress).join(NewsletterMails).filter(NewsletterMails.Newsletter_id==id).all()
    return render_template('admin/viewnewsletter.html', mails=mails, newsletter=newsletter)


@AdminBluePrint.route('/sendnewsletter/<id>')
@roles_accepted("Admin")
def sendnewsletters(id) -> str:
    newsletter = Newsletter.query.filter(Newsletter.NewsletterId==id).first()
    subscribers = Mails.query.filter(Mails.IsActive==1).all()

    for sub in subscribers:
        mail = Mail()
        msg = Message(f"{newsletter.Title}", sender="StefansSuperShop", recipients=[sub.Epostadress])
        msg.body = f"{newsletter.Content}"
        mail.send(msg)
        sendto = NewsletterMails()
        sendto.Newsletter_id = newsletter.NewsletterId
        sendto.Mail_id = sub.EpostID
        newsletter.HasBeenSent = True
        db.session.add(sendto)
        db.session.commit()
    return redirect(url_for('Admin.allnewsletters'))