import math
from flask import request, render_template
from flask_cors import cross_origin
from app.problems.problem_generator import ProblemGenerator
from . import app, db
from .models import User, Quiz, Question
from .auth import basic_auth, token_auth

## BASIC ROUTES TO TEST PROBLEM GENERATION

@app.route("/")
def index():
    gen = ProblemGenerator()
    return gen.mult12()


@app.route("/practice/mult")
def mult():
    gen = ProblemGenerator()
    problem = gen.mult12()
    return render_template("mult.html", data=problem)


@app.route("/practice/add")
def add():
    gen = ProblemGenerator()
    problem = gen.add1()
    return render_template("add.html", data=problem)


@app.route("/practice/add/<int:n>")
def addn(n):
    gen = ProblemGenerator()
    problem = gen.addndigit(n)
    return render_template("add.html", data=problem)


# This route will create a quiz along with N questions to go along with it
# However, this data will NOT YET be part of the database.
@app.route("/quiz/<int:category>/<int:amount>", methods=["GET"])
@token_auth.login_required
def quiz(category, amount):
    current_user = token_auth.current_user()
    pg = ProblemGenerator()
    questions = []
    for _ in range(amount):
        question = pg.new_problem(category)
        questions.append(question)

    return {
        "userId" : current_user.id,
        "category" : category,
        "totalQuestions" : amount,
        "questions" : questions
    }

# On completion of a quiz, whether it is complete or not, this will add the quiz to the db
# and update the points on the user and score of the quiz as well
# this does the bulk of the updating in terms of keeping track of scores
@app.route("/quiz/submit", methods=["POST"])
@token_auth.login_required
def quiz_submit():
    pg = ProblemGenerator()
    current_user = token_auth.current_user()
    if not request.is_json:
        return {'error', "Your content type must be application/JSON"}, 400
    
    data = request.json
    required_fields = ["userId", "category", "questions"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error' : f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    new_quiz = Quiz(category=data['category'], user_id=data['userId'], total_questions=data['totalQuestions'])
    new_quiz_id = new_quiz.id
    qs = []
    quiz_score = 0
    correct_count = 0
    attempt_count = 0
    for q in data['questions']:
        if q.get('response'):
            attempt_count += 1
            is_correct = pg.checkAnswer(q['answer'], q['response'])
            if is_correct:
                correct_count += 1
                quiz_score += q.get('value', 0)
            new_question = Question(prompt=q['prompt'], answer=q['answer'], response=q['response'], quiz_id=new_quiz_id, correct=is_correct, value=q.get('value', 0))
            qs.append(new_question.to_dict())
    new_quiz.score = quiz_score
    new_quiz.total_correct = correct_count
    new_quiz.total_attempted = attempt_count
    new_quiz.save()
    if not current_user.points:
        current_user.points = quiz_score
    else:
        current_user.points = round(float(current_user.points) + quiz_score,2)
    current_user.save()
    return {"quiz" : new_quiz.to_dict(), "questions" : qs}, 200


## LOGIN / SIGNUP ROUTES

@app.route("/signup", methods=["POST"])
def signup():
    if not request.is_json:
        return {'error': 'Content must be a JSON'}, 400
    data = request.json
    required_fields = {"username", "password"}
    missing = []
    for field in required_fields:
        if field not in data:
            missing.append(field)
    if missing:
        return {"error" : f"Fields {', '.join(missing)} must be in the request"}, 400
    
    username = data.get("username")
    password = data.get("password")

    new_user = User(username=username, password=password, points=0)
    return new_user.to_dict(), 201


@app.route("/login")
@basic_auth.login_required
def login():
    user = basic_auth.current_user()
    return user.get_token()




## ROUTES CONCERNING QUESTIONS

# Sends back all questions in db
@app.route("/questions")
def questions():
    select_stmt = db.select(Question)
    data = db.session.execute(select_stmt).scalars().all()
    return [q.to_dict() for q in data], 200

# temporary route that shows what questions are correct / incorrect
@app.route("/questions/graded")
def questions_graded():
    pg = ProblemGenerator()
    select_stmt = db.select(Question)
    data = db.session.execute(select_stmt).scalars().all()
    question_list = [q.to_dict() for q in data]
    grades = []
    for question in question_list:
        grade = {}
        grade['grade'] = pg.checkAnswer(question['answer'], question['response'])
        grade['prompt'] = question['prompt']
        grade['response'] = question['response']
        grade['user'] = question['user']
        grades.append(grade)
    return grades, 200

# This route will return the current user's scores by quiz
@app.route("/my-scores")
@token_auth.login_required
def my_scores():
    current_user = token_auth.current_user()
    return [[quiz.to_dict(), [question.to_dict() for question in quiz.questions]] for quiz in current_user.quizzes]


@app.route("/highscores")
def most_correct():
    users = db.session.execute(db.select(User).where(User.points > 0)).scalars().all()
    user_list = [{'user':user.username, 'totalCorrect': sum([quiz.total_correct or 0 for quiz in user.quizzes]), 'totalQuestions': sum([quiz.total_questions or 0 for quiz in user.quizzes]), 'totalAttempted': sum([quiz.total_attempted or 0 for quiz in user.quizzes]), 'numQuizzes': len(user.quizzes), 'points': user.points} for user in users]

    return sorted(user_list, key=(lambda user: user['points']), reverse=True)
