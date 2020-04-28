from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from . import api
from .errors import forbidden
from app.models import User
from flask import g,request,redirect,url_for
from .users import user_signup

#authentiocation function

from flask import jsonify

@auth.verify_password
def verify_password(email_or_token, password):
    # with out auth access for signup rote only 
    
    print("@@@@@",request.path,request.endpoint)
    if request.values.get('is_sign_up') and request.path=="/getcult/apiV1.0/users/signup/":
        return True
    if request.endpoint=="api.email_token_varify":
        print("verification token")
        return True
    
    
    print(email_or_token,password)
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(user_email_adrs=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)
    
# adding route related to token authentication    
@api.route('/tokens/', methods=['POST'])
def get_token():
    if  g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})

#todo change in stuts code to refer what to do next
@auth.error_handler
def auth_error():
    return forbidden('Invalid credentials',405)


@api.before_request
@auth.login_required
def before_request():
    if request.values.get('is_sign_up') and request.path=="/getcult/apiV1.0/users/signup/":
        return
    if request.endpoint=="api.email_token_varify":
        return 
    if not g.current_user.user_email_verified:
        return forbidden('Unconfirmed account',403)