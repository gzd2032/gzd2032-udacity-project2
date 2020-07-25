# Full Stack Trivia API Backend - Gordon Deng


## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```


REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
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
GET '/questions'
- Fetches a json object that includes a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category, a key pair of the current_category, an array of dictionaries of each question, a key pair of the total number of questions, and a boolean of the success. 
- Request Arguments: None
- Returns: 

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "current_category", 
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
- Deletes a question based on the question id
- Request Arguments: None
- Returns: 

{
  'success': True
}

```
```
POST '/questions'
- Adds a new question to the database
- Request Arguments: {"question": "What?", "answer": "now", "difficulty": 1, "category": 1}
- Returns: 

{
  'success': True
}

```
```
POST '/questions/search'
- Fetches an array of dictionaries of questions that includes a substring of the search term in the question.
- Request Arguments: {"searchTerm":"ss"}
- Returns: 

{
  "current_category": "current_category", 
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
GET '/categories/<int:category_id>/questions'
- Fetches an array of dictionaries of all questions that have particular category id.
- Request Arguments: None
- Returns: 

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
- Fetches a dictionary of a random question based on a specific category id.  If the category id is 0, then the random question is selected from all categories.  If an array of previous question ids are provided, then these questions are excluded from the selection.  If there are available questions to return, then the question dictionary with a false boolean is returned. 
- Request Arguments: {"previous_questions": [], "quiz_category": {"type": "Geography", "id": 2}}
- Returns: 

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