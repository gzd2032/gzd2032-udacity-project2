# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

example setup using virtual env
``` virtual env
source ~/project/starter/env/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create a database name trivia, then restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

# TODO update endpoints REVIEW_COMMENT


Endpoints
```
GET '/categories'
GET '/questions?page=<int>'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
POST '/categories/<int:category_id>/questions'
POST '/quizzes'
```

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of key:value pairs e.g. id:category_string.
- An example return:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```


```
GET '/questions?page=<int>'
- Fetches a list of all categories and an array of question objects that includes pagination for every 10 questions.
- Request Arguments: Include the page number by passing a url value with the format "?page=<int>".  
- Excluding the page variable with default to the first page. "?page=1"
- Returns: An object with a three single key pairs (current_category: null, success:boolean, and total_questions:int), a dictionary of categories, that contains a object of id: category_string key:value pairs, a questions array of question objects with the keys "answer", "category", "difficulty", "id", and "question". 
- An example return:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
   {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 16
}

```
```
DELETE '/questions/<int:question_id>'
- Deletes a question based on the question id.
- Request Arguments: Pass an integer in the format "/questions/<int>"
- Returns: A dictionary with "success" as the key and the value as a boolean.
- An example return:

{
  'success': True
}

```
```
POST '/questions'
- Adds a new question to the database and requires the question, answer text, category, and difficulty score.
- Request Arguments: Pass a json object with the format {"question": (string), "answer": (string), "difficulty": (int), "category": (int)}
- Returns: A dictionary with "success" as the key and the value as a boolean.
- An example return:

{
  'success': True
}

```
```
POST '/questions/search'
- Fetches questions that includes a substring of the search term in the question column.  The search term is not case sensitive.
- Request Arguments: Pass a json object with the key "searchTerm" and the value as a string e.g. {"searchTerm": "ss"}
- Returns:  An object with a three single key pairs (current_category: null, success:boolean, and total_questions:int), a questions object that is an array of question objects with the keys "answer", "category", "difficulty", "id", and "question".
- An example return:

{
  "current_category": "", 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

```
```
POST '/categories/<int:category_id>/questions'
- Fetches an array of dictionaries of all questions that have particular category id.
- Request Arguments: Pass an integer in the format "/categories/<int:category_id>/questions" to the url string.
- Returns: An object with the properties "current_category", "success", "total_questions", and a questions object that is an array of question objects with the keys "answer", "category", "difficulty", "id", and "question".

{
  "current_category": 5, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```
```
POST '/quizzes'
- Fetches a random question from a selected category to play the quiz.  If the category id is 0, then the random question is selected from all categories.  If an array of previous question id's is provided, then these questions are excluded from the selection.  If there are no available questions to return, then it returns a key of "question" with a value of false. 
- Request Arguments: Pass a json object with the format {"previous_questions": [(array of integers)], "quiz_category": {"type": (string), "id": (matching category id integer)}}.  For example:  {"previous_questions": [], "quiz_category": {"type": "Geography", "id": 2}}
- Returns: An object with the key value of "success" and a question object with the keys "answer", "category", "difficulty", "id", and "question".
- An example return:

{
  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```