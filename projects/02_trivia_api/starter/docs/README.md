# API DOCUMENTATION FOR TRIVIA API

## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

## Error Handling
All errors are returned as JSON objects in the format below:
```
{
    "success": False,
    "error": 422,
    "message": "unprocessable"
}
```
The API will return four error types when there is any failure and they are:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

## Endpoints
### GET '/categories'
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs

- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

### GET '/questions'
- General: 
    - Returns a list of category objects, current category, a list of question objects, success value and total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: `curl http://127.0.0.1:5000/questions?page=2`
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
  "current_category": "All",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
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
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Blue",
      "category": 2,
      "difficulty": 5,
      "id": 24,
      "question": "What is Nii's favourite color"
    },
    {
      "answer": "Everything some!!",
      "category": 1,
      "difficulty": 5,
      "id": 25,
      "question": "What is Eli's favourite food"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

### GET '/categories/<category_id>/questions'
- General:
    - Returns the current category, a list of question objects in the specified category, success value and total number of questions in that category.
    - Results are paginated in groups of 10.

- Sample: `curl http://127.0.0.1:5000/categories/6/questions`
```
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### DELETE '/questions/{question_id}'
- General:
    - Deletes the question of the given ID if it exist.
    - Returns the ID of the deleted book and success value.

- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`
```
{
  "deleted": 2,
  "success": true
}
```

### POST '/questions'
- General:
    - Creates a new question using the submitted question, answer, difficulty and category.
    - Return the ID of the created question, success value and total questions.

- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"question\": \"This is a question\", \"answer\": \"This is an answer\", \"difficulty\": 4, \"category\": 3}"`
```
{
  "created": 27,
  "success": true,
  "total_questions": 21
}
```

### POST '/questions'
- General:
    - Also allows search for available questions by search term.
    - Returns a list of all questions that include the current category, given term, success value and total number of questions found with the specified term.
    - Results are paginated in groups of 10.

- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"searchTerm\": \"title\"}"`
```
{
  "current_category": "ALL",
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### POST '/quizzes'
- General:
    - Allows user to specify a category
    - Returns questions for user to answer based on specified category and success value
    - Returns a score after answering 5 questions (This can only be seen on the frontend)

- Sample: `curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d "{\"previous_questions\": [0], \"quiz_category\": {\"type\": \"Art\", \"id\": 2}}"`
```
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}
```































