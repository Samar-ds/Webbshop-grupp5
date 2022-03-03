from flask import Blueprint, request
from models import Mails, db
from flask import jsonify

apiNewsletterBluePrint = Blueprint('apinewsletter', __name__)

class SubscriberApiModel:
    EpostID = 0
    Epostadress = ""
    IsActive = False

# class NewsletterApiModel:
#     NewsletterId = 0
#     Title = ""
#     Content = ""
#     HasBeenSent = False

def _mapSubscriberToApi(subscriber):
    subscriberAPI = SubscriberApiModel()
    subscriberAPI.EpostID = subscriber.EpostID
    subscriberAPI.Epostadress = subscriber.Epostadress
    subscriberAPI.IsActive = subscriber.IsActive
    return subscriberAPI

# def _mapAccountToApi(newsletter):
#     newsletterAPI = NewsletterApiModel()
#     newsletterAPI.NewsletterId = newsletter.NewsletterId
#     newsletterAPI.Title = newsletter.Title
#     newsletterAPI.Content = newsletter.Content
#     newsletterAPI.HasBeenSent = newsletter.HasBeenSent
#     return newsletterAPI

@apiNewsletterBluePrint.route('/api/newsletter/subscribe/<email>', methods=["GET"])
def SubscribeForNewsletterAPI(email):
    if Mails.query.filter(Mails.Epostadress==email).filter(Mails.IsActive==1).first():
        return jsonify(f"{email} already subscribes")
    mail = Mails.query.filter(Mails.Epostadress==email).filter(Mails.IsActive==0).first()
    if mail:
        mail.IsActive = True
        db.session.commit()
        return {"Welcome back!": email}
    new = Mails()
    new.Epostadress = email
    new.IsActive = True
    db.session.add(new)
    db.session.commit()
    return {"New subscriber": email}

@apiNewsletterBluePrint.route('/api/newsletter/unsubscribe/<email>', methods=["GET"])
def UnsubscribeForNewsletterAPI(email):
    mail = Mails.query.filter(Mails.Epostadress==email).first()
    if not mail or mail.IsActive == False:
        return jsonify(f"{email} is already not a subscriber")
    mail.IsActive = False
    db.session.commit()
    return {"Unsubscribed": email}

#/api/newsletter/listsubscribers?top=10&skip=100

@apiNewsletterBluePrint.route("/api/newsletter/listsubscribers", methods=["GET"])
def ListSubscribersAPI():
    top = request.args.get("top", default=2, type=int)
    skip = request.args.get("skip", default=2, type=int)
    subscribers = []
    subs = Mails.query.filter(Mails.IsActive==1).limit(top).offset(skip).all()
    if not subs:
        return {"Error": "Subscribers do not exist","Top": top, "skip": skip}
    for s in subs:
        sub = _mapSubscriberToApi(s)
        subscribers.append(sub)
    return jsonify([subscriber.__dict__ for subscriber in subscribers ])