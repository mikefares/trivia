import json
import os
from select import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from settings import DB_NAME, DB_USER, DB_PASSWORD

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
      response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    
    format_categories = {}
    for categ in categories:
      format_categories[categ.id] = categ.type
    
    if len(format_categories) == 0:
      abort(404)

    return jsonify({
      "categories": format_categories
    })
  


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
  def get_questions():
    categories = Category.query.order_by(Category.id).all()

    selection = Question.query.order_by(Question.id).all()    
    questions = paginate(request, selection)

    format_categories = {}
    for categ in categories:
      format_categories[categ.id] = categ.type

    if len(questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(selection),
      'categories': format_categories,
      'current_category': 'All'
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try: 
      question = Question.query.filter_by(id=question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        "success": True,
        "deleted": question_id
      })
    except:
      abort(422)

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
  def create_new_question():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    new_difficulty = body.get("difficulty", 1)
    new_category = body.get("category", "Science")
    search = body.get("searchTerm", None)


    try: 
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))

        questions = paginate(request, selection)

        return jsonify({
          "success": True,
          "questions": questions,
          "total_questions": len(selection.all()),
          "current_category": "ALL"
        })

      else:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        selection = Question.query.all()

        return jsonify({
          "success": True,
          "created": question.id,
          "total_questions": len(selection)
        })


    except:
      abort(422)

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
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_id(category_id):
    category = Category.query.filter_by(id=category_id).one_or_none()

    if category is None:
      abort(404)
      
    current_category = category.type

    try:
      selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
      questions = paginate(request, selection)

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': current_category
      })

    except:
      abort(422)

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
  def play_quiz(): 
    try:
      body = request.get_json()

      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')

      if quiz_category['id']:
        selection = Question.query.filter_by(category = quiz_category['id']).all()

      else:
        selection = Question.query.all()
      
      ids = [question.id for question in selection]
      randomized = random.choice([number for number in ids if number not in previous_questions])
      
      next_question = Question.query.filter_by(id = randomized).one_or_none()
      previous_questions += ({next_question.id})
      
      return jsonify({
        'success': True,
        'question': next_question.format()
      })

    except:
      abort(422)

    




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}),400

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({"success": False, "error": 405, "message": "method not allowed"}),405
  
  return app

    