from . import api
from flask import jsonify

@api.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

@api.errorhandler(500)
def page_not_found(e):
    response = jsonify({'INternal-error': 'something went wrong'})
    response.status_code = 500
    return response
    

def forbidden(message,code):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = code
    return response

