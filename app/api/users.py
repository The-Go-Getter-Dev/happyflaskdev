from . import api

from app.emails import  send_email


@api.route("/",methods=['GET'])
def get_users():
    return {"hi with authentications":34343}
