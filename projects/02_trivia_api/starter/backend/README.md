# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
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

## Tasks Completed:

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


##  Endpoints documentation: 
### categories :
#### /categroies [ GET ] 
This endpoint is used to get the available questions  
examples usage : 
```
$ curl -X GET localhost:5000/categories
```
Sample result:

```{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```
#### /categories/<int:cat_id>/questions [GET]
This endpoint is used to get the questions associated with a specific cateogry (cat_id) , you can check the category ids form [/categories] endpoint.  
example usage:
```
curl -X GET localhost:5000/categories/1/questions
```
Sample result:
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
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```
### Questions
#### /questions [GET , POST]
##### listing questions:
use *GET* to get a list of all questions availabe in the database , note that this endpoint uses pagination using *page* parameter,so you will only recieve maximum 10 entries per request.  

example usage:  
```
curl -X GET localhost:5000/questions?page=1
```
sample output:
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
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    ...
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
  ], 
  "success": true, 
  "total_questions": 18
}

```
##### Searching questions:
use *POST* In order to find questions that contains a specific keyword , this route expects a json data {"searchTerm" : < your-keyword >}  
  example usage:
  ```
  curl -X POST http://localhost:5000/questions --data '{"searchTerm":"actor"}' --header "Content-Type: application/json" 
  ```
  sample output:
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
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```
 
 ##### Creating a new question
 use *POST* request to this endpoint in order to create a new question , it expects a json with the follwoing format:
 ```
  {"question":"<string>","answer":"<stringr>","difficulty":<int>,"category":<int>}
 ```
example usage:
```
curl -X POST http://localhost:5000/questions --data ' {"question":"test question?","answer":"test answer","difficulty":1,"category":1}' --header "Content-Type: application/json"
```
if the request was successful , you will recieve a json with the new question id and success status
```
{
  "created": 25, 
  "success": true
}

```
#### /questions/<int:question_id>
##### Deleting a question
use *DELETE* request to this endpoint in order to delete a question 
example usage : 
```
curl -X DELETE http://localhost:5000/questions/25 

```
if deletion is successfult , you will recieve a json specifying success status and confirming the deleted question id
```
{
  "deleted": 25, 
  "success": true
}

```
the endpoint will return 404 for non existent questions.

### Quizzes
#### /quizzes [POST]
##### Playing a quiz
use *POST* requests to this endpoint in order to recieve a unique question for your quiz , it expects the following json structure:
```
{"previous_questions":[<int:questions_ids>],"quiz_category":{"type":"<string>","id":"<int>"}}
```
Note : use id:"0" for ALL categories   
example request:
```
curl -X POST http://localhost:5000/quizzes --data '{"previous_questions":[],"quiz_category":{"type":"click","id":"0"}}' --header "Content-Type: application/json" 

```
sample result:
```
{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}

```
if there are no more unique questions , question field in the json will be set to None ; letting you know that the quiz is over.  

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
