import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format("postgres@localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """ Test getting a list of categories """
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_misspelled_category(self):
        """ Test misspelling the end point """
        res = self.client().get("/category")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource Not Found")


    def test_get_questions(self):
        """Test getting a list of questions """
        res = self.client().get("/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])

    def test_get_page_questions(self):
        """Test getting a page of questions"""
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])        

    def test_get_page_questions_error(self):
        """Test getting a not found page"""
        res = self.client().get("/questions?page=999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    def test_add_question(self):
        """Test adding a question"""
        data = {"question":"hellow", "answer":"test", "category":5, "difficulty":3}
        # https://riptutorial.com/flask/example/5622/testing-a-json-api-implemented-in-flask
        res = self.client().post("/questions", data=json.dumps(data), content_type="application/json")

        self.assertEqual(res.status_code, 200)
        new_question = Question.query.get(24)
        question = new_question.format()
        self.assertEqual(question["question"], data["question"])
        self.assertEqual(question["answer"], data["answer"])
        self.assertEqual(question["difficulty"], data["difficulty"])
        self.assertEqual(question["category"], data["category"])
     
    def test_add_question_error(self):
        """Test adding a question error"""
        send_data = {"question":"", "answer":"", "category": "", "difficulty":3}
        # https://riptutorial.com/flask/example/5622/testing-a-json-api-implemented-in-flask
        res = self.client().post("/questions", data=json.dumps(send_data), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    def test_delete_question(self):
        """Test deleting a question """
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_question_error(self):
        """Test deleting a question """
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_search(self):
        """Test searching for questions"""
        send_data = {"searchTerm":"ab"}
        res = self.client().post("/questions/search", data=json.dumps(send_data), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_get_category_questions(self):
        """Test getting questions based on the category"""
        category = "3"
        res = self.client().get("/categories/"+ category + "/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        
    def test_get_category_questions_error(self):
        """Test getting questions based on the category"""
        category = "99"
        res = self.client().get("/categories/"+ category + "/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_quizzes_one_category(self):
        """Test playing quiz by retrieving a question"""
        quiz_category = {"type": "Science", "id": "1"}
        previous_questions = []
        send_data = {"quiz_category": quiz_category, "previous_questions": previous_questions}
        res = self.client().post("/quizzes", data = json.dumps(send_data), content_type="application/json")
        data = json.loads(res.data)

        self.assertTrue(data["success"])

        res_question_id = data["question"]["id"]
        expected_question = Question.query.get(res_question_id)
        self.assertEqual(data["question"], expected_question.format())

    def test_quizzes_all_categories(self):
        """Test playing quiz by retrieving a question"""
        quiz_category = {"type": "click", "id": "0"}
        previous_questions = []
        send_data = {"quiz_category": quiz_category, "previous_questions": previous_questions}
        res = self.client().post("/quizzes", data = json.dumps(send_data), content_type="application/json")
        data = json.loads(res.data)

        self.assertTrue(data["success"])
        res_question_id = data["question"]["id"]
        expected_question = Question.query.get(res_question_id)
        self.assertEqual(data["question"], expected_question.format())

    def test_quizzes_error(self):
        """Test playing quiz by retrieving a question"""
        quiz_category = {"type": "", "id": "99"}
        previous_questions = []
        send_data = {"quiz_category": quiz_category, "previous_questions": previous_questions}
        res = self.client().post("/quizzes", data = json.dumps(send_data), content_type="application/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()