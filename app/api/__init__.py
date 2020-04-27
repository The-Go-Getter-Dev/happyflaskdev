from flask import Blueprint
api = Blueprint('api', __name__)


from . import errors,users ,posts,ratings,cults,authentication,decorators
