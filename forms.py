from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Length, EqualTo


# Forms:
class LoginForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !')])

class RegisterForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired('username is required !'), Length(min=10, max=25, message='username must be between 10 and 25 characters long !')])
    password = PasswordField('Password', validators=[InputRequired('password is required !'), Length(min=8, max=12, message='password must be between 8 and 12 characters long !'), EqualTo('confirm', message='passwords must match !')])
    confirm = PasswordField('Repeat Password')

class EditProfileForm(FlaskForm):
    name = TextField('Name', validators=[InputRequired('name is required !'), Length(min=4, max=50, message='name must be between 4 and 50 characters long !')])
    surname = TextField('Surname', validators=[InputRequired('surname is required !'), Length(min=4, max=50, message='surname must be between 4 and 50 characters long !')])
    avatar = FileField('Avatar', validators=[FileRequired(message='avatar is required !'), FileAllowed(['jpg'], 'images only!')])
    description = TextAreaField('Description', validators=[InputRequired('description is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])
    skills = TextAreaField('Skills', validators=[InputRequired('skills field is required !'), Length(min=2, max=1500, message='skills field must be between 2 and 1500 characters long !')])

class CourseForm(FlaskForm):
    title = TextField('Title', validators=[InputRequired('title is required !'), Length(min=4, max=50, message='name must be between 5 and 500 characters long !')])
    thumbnail = FileField('Thumbnail', validators=[FileRequired(message='thumbnail is required !'), FileAllowed(['jpg'], 'images only!')])
    description = TextAreaField('Description', validators=[InputRequired('description field is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])
    required_skills  = TextAreaField('Required skills', validators=[InputRequired('required skills are required !'), Length(min=2, max=1500, message='required skills must be between 2 and 1500 characters long !')])

class AddSkillsForm(FlaskForm):
    new_skills = TextAreaField('Skills', validators=[InputRequired('skills field is required !'), Length(min=2, max=1500, message='skills field must be between 2 and 1500 characters long !')])

class EditSkillsForm(FlaskForm):
    updated_skills = TextAreaField('Skills', validators=[InputRequired('skills field is required !'), Length(min=2, max=1500, message='skills field must be between 2 and 1500 characters long !')])

class EditAvatarForm(FlaskForm):
    new_avatar = FileField('Avatar', validators=[FileRequired(message='avatar is required !'), FileAllowed(['jpg'], 'images only!')])

class EditFullNameForm(FlaskForm):
    new_name = TextField('Name', validators=[InputRequired('name is required !'), Length(min=4, max=50, message='name must be between 4 and 50 characters long !')])
    new_surname = TextField('Surname', validators=[InputRequired('surname is required !'), Length(min=4, max=50, message='surname must be between 4 and 50 characters long !')])

class AddDescription(FlaskForm):
    extra_descr = TextAreaField('Description', validators=[InputRequired('description field is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])

class EditDescription(FlaskForm):
    new_descr = TextAreaField('Description', validators=[InputRequired('description field is required !'), Length(min=10, max=1500, message='description must be between 10 and 1500 characters long !')])
