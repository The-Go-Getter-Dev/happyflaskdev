from . import api
from flask import g,current_app,request,url_for
from app.emails import  send_email
from sqlalchemy.exc import IntegrityError
from flask import jsonify,g
from app.models import Post
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
token_serializer=URLSafeTimedSerializer('Key from the universe Secret')
from app import db


@api.route("/posts/<int:id>")
def get_post_content(id):
    post=Post.query.get(id)
    return post.get_post_data()

@api.route("/posts/")
def get_posts():
    post_dict={}
    post_num=0
    return{ post.id:post.get_post_data() for post in Post.query.all()},200

@api.route("/posts/create/",methods=['POST'])
def create_post():
    poster=g.current_user
    post_from_cult=None
    data=request.values
    new_post=None
    # adding only founder to right post
    if poster.user_if_Founder:
        post_from_cult=poster.user_founder_cult
        try:
            new_post=Post.post_creation(data,post_from_cult)
        except IntegrityError:
            return {"status":"invalid credentials create"},404
        return new_post.get_compact_data()
    return {"status":"not allowd topost"},203