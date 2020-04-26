from datetime import datetime
from flask import render_template, session, redirect, url_for,request
from . import main
import psycopg2
#from app.main.forms import NameForm
from app import db
from app.emails import send_email
from app.models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    req_data=request.form
    if req_data.get("user_name") != None:
        if User.query.filter_by(user_name=req_data.get("user_name")).first() == None:
            new_user=User(user_name=req_data.get("user_name"),user_image=request.files.get("image").read())
            db.session.add(new_user)
            db.session.commit()
            salutation="hi-NewUser{}".format(req_data.get("user_name"))
            send_email(salutation,"marblelabs.in@gmail.com",["kparashar172@gmail.com"],"hi kio","<h1>hello kioplolo</h1>")
    return{'req':str(req_data.get("user_name")),"heeloo from th blurpints":str(datetime.utcnow())}


@main.route('/user/<int:id>')
def get_user(id):
    usr=User.query.filter_by(id=id).first()
    user_data={}
    user_data['user_img']=usr.user_image.write()
    user_data['user_name']=usr.user_name
    return user_data