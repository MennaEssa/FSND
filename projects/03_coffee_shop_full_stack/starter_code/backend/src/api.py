import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO_DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO_DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks' , methods=['GET'])
def list_drinks():
    drinks = Drink.query.all()
    return jsonify ({
        'success': True,
        'drinks' : [ drink.short() for drink in drinks ]
    })


'''
@TODO_DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail' , methods=['GET'])
@requires_auth(permission="get:drinks-detail")
def list_drinks_details():
    drinks = Drink.query.all()
    return jsonify ({
        'success': True,
        'drinks' : [ drink.long() for drink in drinks ]
    })


'''
@TODO_DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure'
'''
@app.route('/drinks' , methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drink():
    try:
        drink_request = request.get_json()
        print(drink_request)
    except Exception as e:
        print(str(e))
        abort(400)    
    try:
        new_drink=Drink( title = drink_request['title'],
                         recipe = json.dumps(drink_request['recipe']))
        new_drink.insert()
    except KeyError as e:
        print(str(e))
        abort(400)
    except exc.IntegrityError:
        return jsonify(
            {
                'success':False,
                'message': "This drink name already exists",
                'error' : 422
            },422
        )


    return jsonify({'success':True,
                    'drinks': [new_drink.long()] 
                   })

'''
@TODO_DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>' , methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drink(drink_id):
    drink_request = request.get_json()
    drink=Drink.query.get(drink_id)
    if(drink is None):
        abort(404)
    if 'title' in drink_request:
        drink.title = drink_request['title']
    if 'recipe' in drink_request:
        drink.recipe = json.dumps(drink_request['recipe'])
    drink.update()
    
    return jsonify({
        'success':True,
        'drinks' : [ drink.long() ]
    })
    
'''
@TODO_DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>" , methods=['DELETE'])
@requires_auth(permission="delete:drinks")
def delete_drink(drink_id):
    drink=Drink.query.get(drink_id)
    if(drink is None):
        abort(404)
    
    drink.delete()
    return jsonify({
        'success':True,
        'delete' : drink_id
    })


## Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO_DONE implement error handlers using the @app.errorhandler(error) decorator 
for error 404
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
          }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
            "success": False, 
            "error": 400,
            "message": "malformed request"
          }), 400

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success":False,
        "error" : error.status_code,
        "message": error.error["description"]
    }) , error.status_code