import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sys import exc_info
import random
from models import setup_db, Question, Category
from werkzeug.exceptions import NotFound , InternalServerError , UnprocessableEntity
QUESTIONS_PER_PAGE = 10


def paginate(request , query_result):
  '''
  enables pagination a query result as defined in the global variable QUESTIONS_PER_PAGE
  @param request : the request send to the endpoint
  @param query_result : the result of the query you need to paginate ; this was written of 
        the questions query but it should work on queries from other models as well
  @return a list of predefined size list with the correct starting index.
  '''
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in query_result]
  questions_page = questions[start:end]
  return questions_page

def convert_categories_dict(cat_query_result):
  '''
  the front end requires the categories to be formatted as a dict {id:type}
  so this handles this conversion
  @param categories query result 
  @returns categories dict usable by the frontend
  '''
  cat_dict={}
  for category in cat_query_result:
    cat_dict[category.id] = category.type
  return cat_dict


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)   
  '''
  @TODO_DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app , resources={r"*": {"origins": "*"} })

  '''
  @TODO_DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO_DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories' , methods=['GET'])
  def get_categories():
    cat_dict={}
    try:
      cat_dict = convert_categories_dict(Category.query.all())
    except:
      print(exc_info())
      abort(500)

    return jsonify({
      'success': True ,
      'categories': cat_dict , #[ cat.format() for cat in categories] , 
      'total_categories' : len(cat_dict)
    })
    
  '''
  @TODO_DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions' , methods=['GET'])
  def get_questions():
    questions = Question.query.all()
    current_questions = paginate(request , questions)
    if not current_questions:
      abort(404)

    return jsonify({
      'success':True,
      'questions': current_questions ,
      'total_questions' : len(questions) ,
      'categories': convert_categories_dict(Category.query.all())
    })
    

  '''
  @TODO_DONE: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:q_id>' , methods=['DELETE'])
  def delete_question(q_id):
      question = Question.query.filter(Question.id == q_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success':True,
        'deleted':q_id,
      })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({ 'error':500,
             'success':False,
             'message': 'Internal server error' 
    }) , 500
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({ 'error':422,
              'success':False , 
              'message' : 'could not process request'
    }) , 422


  
  return app

    