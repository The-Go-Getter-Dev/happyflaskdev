from . import api
from flask import g,current_app,request,url_for
from app.emails import  send_email
from sqlalchemy.exc import IntegrityError
from flask import jsonify,g
from app.models import Cult
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
token_serializer=URLSafeTimedSerializer('Key from the universe Secret')
from app import db


@api.route("/cults/")
def get_culs():
    usr=g.current_user
    city=usr.user_city
    cults=Cult.query.filter_by(cult_city=city).all()
    cult_list=[]
    for cult in cults:
        cult_list.append(cult.get_compact_data())
    return jsonify(cult_list)

@api.route("/cults/createcult/",methods=['POST'])
def creat_cult():
    usr=g.current_user
    if usr.user_if_Founder:
        return {"feedback":"Not allowed","message":"alredy founder of cult"},203
    data=request.values
    print(data.get('cult_name'),data.get("cult_quote_line"))
    new_cult=None
    try:
        new_cult=Cult.register_cult(data,usr.id)
    except IntegrityError:
        return {'created':"False"},403
    usr.user_if_Founder=True
    db.session.add(usr)
    db.session.commit()
    
    #user_email=str(data.get("user_email_adrs"))
    #token_generate_and_send_email(user_email,new_user.user_name)
    return {"created":"true","user":new_cult.get_compact_data()},201
