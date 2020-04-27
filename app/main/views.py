from datetime import datetime
from flask import render_template, session, redirect, url_for,request
from . import main
import psycopg2
#from app.main.forms import NameForm
from app import db
from app.emails import send_email
from app.models import User
from itsdangerous import URLSafeTimedSerializer,SignatureExpired,Serializer

token_serializer=URLSafeTimedSerializer("the secret key is here")

@main.route('/', methods=['GET', 'POST'])
def index():
    req_data=request.form
    if req_data.get("user_name") != None:
        if User.query.filter_by(user_name=req_data.get("user_name")).first() == None:
            new_user=User(user_name=req_data.get("user_name"),user_image=request.files.get("image").read(),user_email_adrs=req_data.get("email"),user_password=req_data.get("user_password"))
            db.session.add(new_user)
            db.session.commit()
            email=new_user.user_email_adrs
            email_token=token_serializer.dumps(email,salt='email-confirmation')
            salutation="hi-NewUser{}".format(req_data.get("user_name"))
            text_message='click on the link for account confirm <a href="http://127.0.0.1:5000'+url_for('.email_token_varify',token=email_token)+'"> click to account confirmations</a>'
            htmk_message='click on the link for account confirm <a href="http://127.0.0.1:5000'+url_for('.email_token_varify',token=email_token)+'"> click to account confirmations</a>'
            send_email(salutation,"marblelabs.in@gmail.com",[email],"hi kio"+text_message,"<h1>hello kioplolo<h2>"+htmk_message+"</h2></h1>")
    return{'req':str(req_data.get("user_name")),"heeloo from th blurpints":str(datetime.utcnow()),'token':email_token}

@main.route('/email_token_varify/<string:token>')
def email_token_varify(token):
    try:
        print("token=",token)
        email=token_serializer.loads(token,salt='email-confirmation',max_age=1000)
        print('email=',email)
    except SignatureExpired:
        return '<h1>token is expired</h1>'
    usr=User.query.filter_by(user_email_adrs=email).first()
    usr.user_email_verified=True
    db.session.commit()
    return '<h1>susscess!! you are verifiled user now{}</h1>'.format(usr.user_name)

@main.route('/user/<int:id>')
def get_user(id):
    usr=User.query.filter_by(id=id).first()
    user_data={}
    user_data['user_img']=usr.user_image.write()
    user_data['user_name']=usr.user_name
    return user_data