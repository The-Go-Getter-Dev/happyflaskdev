from . import api
from flask import g,current_app,request,url_for
from app.emails import  send_email
from sqlalchemy.exc import IntegrityError
from flask import jsonify,g
from app.models import User
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
token_serializer=URLSafeTimedSerializer('Key from the universe Secret')
from app import db

@api.route("/",methods=['GET'])
def get_users():
    usr=User.query.all()
    usr
    userschema=Userschema()
    data=userschema.dump(usr[0])
    return jsonify(data)

@api.route("/users/signup/",methods=['POST'])
def user_signup():
    data=request.values
    print(data.get('user_name'),data.get("user_email_adrs"))
    new_user=None
    try:
        new_user=User.register_user(data)
    except IntegrityError:
        return {'created':"False"},403
    user_email=str(data.get("user_email_adrs"))
    token_generate_and_send_email(user_email,new_user.user_name)
    return {"created":"true","user":new_user.user_profile()},201






def token_generate_and_send_email(email,username):
    email_token=token_serializer.dumps(email,salt='email-confirmation')
    salutation="hi-NewUser{}".format(username)
    text_message='click on the link for account confirm <a href="http://127.0.0.1:5000'+url_for('.email_token_varify',token=email_token)+'"> click to account confirmations</a>'
    htmk_message='click on the link for account confirm <a href="http://127.0.0.1:5000'+url_for('.email_token_varify',token=email_token)+'"> click to account confirmations</a>'
    send_email(salutation,"marblelabs.in@gmail.com",[email],"hi kio"+text_message,"<h1>hello kioplolo<h2>"+htmk_message+"</h2></h1>")
    
    
    


@api.route('/email_token_varify/<string:token>')
def email_token_varify(token):
    try:
        print("token=",token)
        email=token_serializer.loads(token,salt='email-confirmation',max_age=(3600*24*3))
        print('email=',email)
    except SignatureExpired:
        return '<h1>token is expired</h1>'
    usr=User.query.filter_by(user_email_adrs=email).first()
    usr.user_email_verified=True
    db.session.commit()
    return '<h1>susscess!! you are verifiled user now{}</h1>'.format(usr.user_name)
