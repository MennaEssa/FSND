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
        self.database_path = database_path = "postgresql:///{}".format(self.database_name)
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
    def test_questions_paginated(self):
        """
        expects a single page with the correct number of questions
        """
        res = self.client().get("/questions")
        data=json.loads(res.data)
        self.assertEqual(res.status_code , 200)
        self.assertEqual(len(data["questions"]) , 10)
        self.assertEqual(data["total_questions"], len(Question.query.all()))

    def test_questions_paginated_error(self):
        """
        if pagination fails because of the page parameter , the client
        should recieve a 404 error instead of crashing the server.
        """
        res = self.client().get("/questions" , query_string={"page": 1000})
        data=json.loads(res.data)
        self.assertEqual(res.status_code , 404)

    
    def test_get_categories(self):
        """
        confirm the correct response format require by the frontend
        """
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code , 200)
        self.assertIsInstance(data["categories"] , dict)
        self.assertEqual(len(data["categories"]) , 6 )
        self.assertEqual(data["total_categories"] , 6 )

    def test_delete_question(self):
        """
        adds a dummy question then attempts to delete it ; verify expected behavior.
        """
        test_q = Question(question="test?" , answer="test" , category=1 , difficulty=1 )
        test_q.insert()
        res = self.client().delete("/questions/"+str(test_q.id))
        self.assertEqual(res.status_code , 200)
        self.assertIsNone(Question.query.get(test_q.id))

    
    def test_delete_question_error(self):
        """
        attempting to delete a question that does not exist should return 404
        """
        res = self.client().delete("/questions/100000000")
        self.assertEqual(res.status_code , 404)
    
    def test_add_question(self):
        """
        verify addition of a new question 
        """
        res = self.client().post("/questions" , json = {"question":"test question?","answer":"test answer","difficulty":1,"category":1})
        self.assertEqual(res.status_code , 200)
        self.assertIsNotNone(Question.query.filter(Question.question == "test question?").all())
    
    def test_add_question_error(self):
        """
        return 422 if a a json data is no processable i.e wrong field name
        """
        res = self.client().post("/questions" , json = {"questionSS":"test question?","answer":"test answer","difficulty":1,"category":1})
        self.assertEqual(res.status_code , 422)
    
    def test_search_question(self):
        res= self.client().post("/questions" , json={"searchTerm":"actor"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["total_questions"],1)
        self.assertEqual(len(data["questions"]) , 1)
    
    def test_search_question_noresults(self):
        res= self.client().post("/questions" , json={"searchTerm":"THISDOESNOTEXIST"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["total_questions"],0)
        self.assertEqual(len(data["questions"]) , 0)
    
    def test_search_question_error(self):
        res= self.client().post("/questions" , json={"searchINGTerm":"actor"})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
    
    def test_question_by_category(self):
        res=self.client().get("/categories/5/questions")
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data["questions"]), 3)
        self.assertEqual(data["total_questions"], 3)
    
    def test_question_by_category_notexist(self):
        res=self.client().get("/categories/10000/questions")
        self.assertEqual(res.status_code,404)
    
    def test_quiz_cat(self):
        """
        test correct behaviour if we select a secific category for the quiz 
        """
        res=self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"type":"Geography","id":"3"}})
        data=json.loads(res.data)
        self.assertEqual(res.status_code , 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["question"]),5)
        self.assertEqual( data["question"]["category"] , 3)
        
    def test_quiz_all(self):
        """
        test correct behaviour if a use ALL  mode in the quiz
        """
        res=self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"type":"click","id":"0"}})
        data=json.loads(res.data)
        self.assertEqual(res.status_code , 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["question"]),5)
        self.assertGreater( data["question"]["category"] , 0)
    
    def test_quiz_error(self):
        """
        test that we get error 422 if a question is requested with a non existent category.
        """
        res=self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"type":"Geography","id":"222222"}})
        data=json.loads(res.data)
        self.assertEqual(res.status_code , 422)


    

        




    

    

        





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()