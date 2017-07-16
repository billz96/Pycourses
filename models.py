from main import db


# Models:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique = True, nullable=False)
    password = db.Column(db.String(32), nullable=False) # hashed password

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '< User: '+self.username+' >'

class LoggedIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique = True, nullable=False)
    rand_id = db.Column(db.String(32), unique = True, nullable=False)

    def __init__(self, username, rand_id):
        self.username = username
        self.rand_id = rand_id
    def __repr__(self):
        return '< LoggedInUser: '+self.username+' >'

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(1500), unique=False, nullable=False)
    avatar = db.Column(db.String(32), unique=False, nullable=False)
    skills = db.Column(db.String(1500), unique=False, nullable=False)

    def __init__(self, user_id, name, surname, avatar, description, skills):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.avatar = avatar
        self.description = description
        self.skills = skills
    def __repr__(self):
        return '< Profile: '+self.user_id+' >'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    title = db.Column(db.String(500), unique=False, nullable=False)
    description = db.Column(db.String(1500), unique=False, nullable=False)
    thumbnail = db.Column(db.String(32), unique=False, nullable=False)
    required_skills = db.Column(db.String(1500), unique=False, nullable=False)
    avg_rating = db.Column(db.Integer, unique=False, nullable=True)
    ratings = db.Column(db.Integer, unique=False, nullable=True)
    enrolled = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, user_id, title, description, thumbnail, required_skills, avg_rating=0, ratings=0, enrolled=0):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.required_skills = required_skills
        self.avg_rating = avg_rating
        self.ratings = ratings
        self.enrolled = enrolled
    def __repr__(self):
        return '< Course: '+self.user_id+' >'

# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, unique=True, nullable=False)
#     course_id = db.Column(db.Integer, unique=True, nullable=False)
#     text = db.Column(db.String(1500), unique=False, nullable=False)
#     stars = db.Column(db.Integer, unique=False, nullable=False)
#
#     def __init__(self, user_id, course_id, text, stars):
#         self.user_id = user_id
#         self.course_id = course_id
#         self.text = text
#         self.stars = stars
    #  def __repr__(self):
    #      return '< Review: '+self.user_id+' >'

# class Lesson(db.Model):
#     ...
#     def __init__(self, user_id, course_id, video, title, description, thumbnail):
#         self.user_id = user_id
#         self.course_id = course_id
#         self.description = description
#         self.thumbnail = thumbnail
#         self.video = video
#         self.title = title
