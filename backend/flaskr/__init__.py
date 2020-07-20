import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * 10
  end = start + QUESTIONS_PER_PAGE
  questions = [questions.format() for questions in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  @app.route('/')
  @cross_origin()
  def home_app():
    return jsonify({
      'success': True,
      'questions': '1'
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  @cross_origin()
  def get_categories():
    try:
      selections = Category.query.all()
      if len(selections) == 0:
        abort(404)
      current_categories = [categories.format() for categories in selections]
      list_of_categories = {}
      for category in current_categories:
        list_of_categories[ category["id"] ] = category["type"]
    
      return jsonify({
        'success': True,
        'categories': list_of_categories
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  @cross_origin()
  def get_questions():
    print("getting questions")
    try:
      selections = Question.query.order_by(Question.id).all()
      categories = Category.query.order_by(Category.id).all()
      if len(categories) == 0:
        abort(404)
      current_questions = paginate_questions(request, selections)
      current_categories = [category.format() for category in categories]
      categories_list = {}
      for category in current_categories:
        categories_list[category['id']] = category['type']

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selections),
        'current_category': 'current_category',
        'categories': categories_list
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  @cross_origin()
  def delete_question(question_id):
    try:
      selection = Question.query.get(question_id)
      selection.delete()

      return jsonify({
        'success': True
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  @cross_origin()
  def add_question():
    entry = request.get_json()
    question = Question(question = entry["question"], answer = entry["answer"], category = entry["difficulty"], difficulty = entry["category"])
    try:
      question.insert()
      print(question.format())
      return jsonify({
        'success': True
      })
    except:
      abort(400)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  @cross_origin()
  def search_questions():
    search_term = request.get_json()["searchTerm"]
    print(search_term)
    try:
      search_result = Question.query.filter(Question.question.ilike('%'+ search_term + '%')).all()
      # if len(search_result) == 0:
      #   abort(404)
      questions = paginate_questions(request, search_result)
      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(search_result),
        'current_category': 'current_category'
      })
    except:
      abort(400)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  @cross_origin()
  def get_by_category(category_id):
    try:
      selection = Question.query.filter(Question.category == category_id).all()
      if len(selection) == 0:
        abort(404)
      current_questions = paginate_questions(request, selection)
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': category_id
      })

    except:
      abort(400)

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

  @app.route('/quizzes', methods=['POST'])
  @cross_origin()
  def start_quiz():
    status = request.get_json()

    category = status["quiz_category"]["id"]
    previous_questions = status["previous_questions"]
    print("Prev: ", previous_questions)
    try:
      if len(previous_questions) == 0:
      # use of not logical operator "~" https://programmer.group/python-sql-alchemy-section-2-query-conditions-settings.html
        selection = Question.query.filter(Question.category == category).all()
      else:
        selection = Question.query.filter(Question.category == category).filter(~Question.id.in_(previous_questions)).all()
      if len(selection) == 0:
        random_question = False
      else:
        questions = paginate_questions(request, selection)
        print("questions", questions)
        # pick list index randomly using randint() from https://pynative.com/python-random-choice/ 
        objectIndex = random.randint(0, len(questions)-1)
        print(objectIndex)
        print(len(questions))
        random_question = questions[objectIndex]
        print(random_question)
      return jsonify({
        'success': True,
        'question': random_question
      })

    except:
      abort(400)
    


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  @cross_origin()
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource Not Found"
    }), 404

  @app.errorhandler(405)
  @cross_origin()
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(422)
  @cross_origin()
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unable to process data"
    }), 422

  @app.errorhandler(400)
  @cross_origin() 
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(500)
  @cross_origin()
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Server Error"
    }), 500

  return app

    