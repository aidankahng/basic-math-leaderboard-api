# REST-ful Math Problem Generator

Math problem API created in Python using Flask, SQL Alchemy, and a PostgreSQL database. Webservice and database are hosted on Render.

### Public Routes:
#### [GET] /random
Example JSON Data:
```
{
    "prompt" : "12 x 7 = ",
    "answer" : "84",
    "value" : 1.3
}
```
#### [GET] /practice/mult
Webpage with single practice problem of the form "a x b = " 
#### [GET] /practice/add
Webpage with single practice problem of the form "a + b = "
#### [GET] /questions
List of all questions answered so far as a JSON
#### [GET] /questions/graded
UNUSED: Shows the correctness of each question answered as a JSON
#### [GET] /highscores
JSON List of users ordered by total points accumulated
Example JSON Data:
```
[
    {
        "clan": "some-clan",
        "message": "Math is fun!",
        "numQuizzes": 6,
        "points": "89.5",
        "totalAttempted": 75,
        "totalCorrect": 73,
        "totalQuestions": 75,
        "user": "testUser123"
    },
    {
        "clan": "noclan",
        "message": "Why is 0! = 1?",
        "numQuizzes": 3,
        "points": "64.2",
        "totalAttempted": 30,
        "totalCorrect": 24,
        "totalQuestions": 30,
        "user": "anotherUser"
    }, ...
]
```
#### [POST] /sign-up
