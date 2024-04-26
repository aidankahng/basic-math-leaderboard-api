from datetime import datetime, timedelta, timezone
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# User class holds the info associated with the user including a token for verification purposes
# ID, Username, Password, Token
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    points = db.Column(db.Numeric)
    message = db.Column(db.String)
    clan = db.Column(db.String)


    token = db.Column(db.String, index=True, unique=True)
    token_expiration = db.Column(db.DateTime(timezone=True))

    quizzes = db.relationship('Quiz', back_populates='user')


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_password(self.password)
        self.save()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)
    
    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)
    
    def edit(self, new_username, plaintext_password, message, clan):
        if new_username != '':
            self.username = new_username
        if message != '':
            self.message = message
        if clan != '':
            self.clan = clan
        if plaintext_password != '':
            self.set_password(plaintext_password)
        self.save()
    
    def to_dict(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "points" : self.points,
            "quizzes" : [s.to_dict() for s in self.quizzes]
        }
    
    def get_token(self):
        now = datetime.now(timezone.utc)
        if self.token and (self.token_expiration > now + timedelta(hours = 1)):
            return {'token' : self.token}
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(days=31)
        self.save()
        return {
            "token" : self.token,
            "tokenExpiration" : self.token_expiration
        }



# Quiz table will hold information about how users have done in the past.
# One user -> many Quiz, one Quiz -> many problems
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer, nullable=False)
    quiz_style = db.Column(db.String)
    total_questions = db.Column(db.Integer)
    total_correct = db.Column(db.Integer)
    total_attempted = db.Column(db.Integer)
    score = db.Column(db.Numeric)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.save()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            "id" : self.id,
            "category" : self.category,
            "quizStyle" : self.quiz_style,
            "totalQuestions" : self.total_questions,
            "totalCorrect" : self.total_correct,
            "totalAttempted" : self.total_attempted,
            "score" : self.score,
            "userId" : self.user_id,
            "user" : self.user.username
        }

# Question table will hold information about all questions that have been attempted.
# each question will be associated with a session
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    response = db.Column(db.String, nullable=False)
    correct = db.Column(db.Boolean)
    value = db.Column(db.Numeric)


    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    quiz = db.relationship('Quiz', back_populates='questions')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            "id" : self.id,
            "prompt" : self.prompt,
            "answer" : self.answer,
            "response" : self.response,
            "correct" : self.correct,
            "value" : self.value,
            "quizId" : self.quiz_id,
            "user" : self.quiz.user.username,
        }