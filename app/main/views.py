from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
#from app.main.forms import NameForm
from app import db
from app.emails import send_email
from app.models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    send_email("hi-there","marblelabs.in@gmail.com",["kparashar172@gmail.com"],"hi kio","<h1>hello kioplolo</h1>")
    return{"heeloo from th blurpints":str(datetime.utcnow())}

