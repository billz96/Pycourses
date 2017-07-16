from main import app, APP_ROOT, db
from flask import render_template, request, session, redirect, url_for
from os import path, mkdir, remove
from werkzeug.utils import secure_filename
from helpers import loggedIn, randId, logoutUser
from bcrypt import hashpw, gensalt
from models import User, LoggedIn, Profile, Course
from forms import LoginForm, RegisterForm, EditProfileForm, CourseForm, AddSkillsForm, EditSkillsForm, EditAvatarForm, EditFullNameForm, EditDescription, AddDescription



# Views:
@app.route('/', methods=['GET'])
def home():
   username = loggedIn(session, LoggedIn)
   if username == False:
       form = LoginForm()
       return render_template('login.html', form=form)
   else:
       return render_template('index.html', username=username)



@app.route('/delete-course/<id>', methods=['GET'])
def del_course(id):
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)


    # delete thumbnail
    course = Course.query.filter_by(id=id).first()
    target = path.join(APP_ROOT, 'static/courses/')
    file_path = path.join(target, course.thumbnail)
    remove(file_path)

    # delete course
    db.session.delete(course)
    db.session.commit()

    # render my course page
    user = User.query.filter_by(username=username).first()
    courses = Course.query.filter_by(user_id=user.id).all()
    return render_template('my_courses.html', username=username, courses=courses)



@app.route('/add-descr', methods=['POST'])
def add_descr():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    a_skills = AddSkillsForm()
    e_skills = EditSkillsForm()
    e_avatar = EditAvatarForm()
    e_descr = EditDescription()
    e_flname = EditFullNameForm()

    a_descr = AddDescription()
    if a_descr.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # add and save description
        if user_profile.description == 'no-description':
            user_profile.description = request.form['extra_descr']
        else:
            user_profile.description += request.form['extra_descr']
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    # render edit profile pages
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/edit-descr', methods=['POST'])
def edit_descr():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    a_skills = AddSkillsForm()
    e_skills = EditSkillsForm()
    e_avatar = EditAvatarForm()
    a_descr = AddDescription()
    e_flname = EditFullNameForm()

    e_descr = EditDescription()
    if e_descr.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # edit and save description
        user_profile.description = request.form['new_descr']
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    # render edit profile pages
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/edit-fullname', methods=['POST'])
def edit_flname():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    a_skills = AddSkillsForm()
    e_skills = EditSkillsForm()
    e_avatar = EditAvatarForm()
    e_descr = EditDescription()
    a_descr = AddDescription()

    e_flname = EditFullNameForm()
    if e_flname.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # change skills
        user_profile.name = request.form['new_name']
        user_profile.surname = request.form['new_surname']
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    # render edit profile pages
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/edit-avatar', methods=['POST'])
def edit_avatar():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    a_skills = AddSkillsForm()
    e_skills = EditSkillsForm()
    e_flname = EditFullNameForm()
    e_descr = EditDescription()
    a_descr = AddDescription()

    e_avatar = EditAvatarForm()
    if e_avatar.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # update avatar
        new_avatar = e_avatar.new_avatar.data
        filename = secure_filename(new_avatar.filename)

        rand_ID = str(randId())
        while True:
            result = Profile.query.filter_by(avatar=rand_ID).first()
            if result:
                rand_ID = str(randId())
            else:
                break

        filename = ''+rand_ID+'.jpg' # ex: filename = ekjenrfueorf.jpg
        target = path.join(APP_ROOT, 'static/avatars/')
        if not path.isdir(target):
            mkdir(target)

        old_path = path.join(target, user_profile.avatar)
        new_path = path.join(target, filename)

        if user_profile.avatar != "saitama-batman.jpg":
            remove(old_path)

        new_avatar.save(new_path)
        user_profile.avatar = filename
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    # render edit profile pages
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/edit-skills', methods=['POST'])
def edit_skills():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    a_skills = AddSkillsForm()
    e_avatar = EditAvatarForm()
    e_flname = EditFullNameForm()
    e_descr = EditDescription()
    a_descr = AddDescription()

    e_skills = EditSkillsForm()
    if e_skills.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # change skills
        user_profile.skills = request.form['updated_skills']
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)


    # render edit profile pages
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)


@app.route('/add-skills', methods=['POST'])
def add_skills():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = EditProfileForm()
    e_skills = EditSkillsForm()
    e_avatar = EditAvatarForm()
    e_flname = EditFullNameForm()
    e_descr = EditDescription()
    a_descr = AddDescription()

    a_skills = AddSkillsForm()
    if a_skills.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # change profile and save
        if user_profile.skills == 'no-skills':
            user_profile.skills = request.form['new_skills']
        else:
            user_profile.skills += request.form['new_skills']
        db.session.commit()

        # render profile page
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    # render edit profile page
    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/my-courses', methods=['GET'])
def my_courses():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    user = User.query.filter_by(username=username).first()
    courses = Course.query.filter_by(user_id=user.id).all()
    return render_template('my_courses.html', username=username, courses=courses)



@app.route('/new-course', methods=['GET', 'POST'])
def course():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    form = CourseForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        # save thumbnail
        thumbnail = form.thumbnail.data
        filename = secure_filename(thumbnail.filename)

        rand_ID = str(randId())
        while True:
            result = Course.query.filter_by(thumbnail=rand_ID).first()
            if result:
                rand_ID = str(randId())
            else:
                break

        filename = ''+rand_ID+'.jpg'
        target = path.join(APP_ROOT, 'static/courses/')
        if not path.isdir(target):
            mkdir(target)

        thumbnail.save(path.join(target, filename))

        # save course
        title = request.form['title']
        description = request.form['description']
        required_skills = request.form['required_skills']
        course = Course(user_id=user.id, title=title, description=description, thumbnail=filename, required_skills=required_skills)
        db.session.add(course)
        db.session.commit()

        return render_template('index.html', username=username)

    return render_template('new_course.html', form=form)



@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    # AddSkillsForm, EditSkillsForm, EditAvatarForm, EditFullNameForm
    a_skills = AddSkillsForm()
    e_skills = EditSkillsForm()
    e_avatar = EditAvatarForm()
    e_flname = EditFullNameForm()
    e_descr = EditDescription()
    a_descr = AddDescription()

    form = EditProfileForm()
    if form.validate_on_submit():
        # find user by username and his/her profile by his/her id
        user = User.query.filter_by(username=username).first()
        user_profile = Profile.query.filter_by(user_id=user.id).first()

        # update current user's profile data
        user_profile.name = request.form['name']
        user_profile.surname = request.form['surname']
        user_profile.description = request.form['description']
        user_profile.skills = request.form['skills']

        # update avatar
        avatar = form.avatar.data
        filename = secure_filename(avatar.filename) # maybe it's optional because i change the filename

        rand_ID = str(randId())
        while True:
            result = Profile.query.filter_by(avatar=rand_ID).first()
            if result:
                rand_ID = str(randId())
            else:
                break

        filename = ''+rand_ID+'.jpg'
        target = path.join(APP_ROOT, 'static/avatars/') # target = project's path + /static/avatars
        if not path.isdir(target): # if target doesn't exist
            mkdir(target) # we create the target

        old_path = path.join(target, user_profile.avatar)
        new_path = path.join(target, filename)

        if user_profile.avatar != "saitama-batman.jpg":
            remove(old_path)

        avatar.save(new_path) # save the file in the target
        user_profile.avatar = filename

        # save changes in profile table
        db.session.commit()
        user_skills = user_profile.skills.split(',')
        return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)

    return render_template('edit_profile.html', form=form, a_skills=a_skills, e_skills=e_skills, e_avatar=e_avatar, e_flname=e_flname, e_descr=e_descr, a_descr=a_descr)



@app.route('/profile', methods=['GET'])
def profile():
    username = loggedIn(session, LoggedIn)
    if username == False:
        form = LoginForm()
        return render_template('login.html', form=form)

    user = User.query.filter_by(username=username).first()
    user_profile = Profile.query.filter_by(user_id=user.id).first()
    user_skills = user_profile.skills.split(',')
    return render_template('profile.html', username=username, user_profile=user_profile, user_skills=user_skills)



@app.route('/register', methods=['GET', 'POST'])
def register():
    username = loggedIn(session, LoggedIn)
    if username != False:
        return render_template('index.html', username=username)

    form = RegisterForm()
    if form.validate_on_submit():
        hashedPwd = hashpw(str(request.form['password']).encode('utf-8'), gensalt()) # encrypt user's password
        user = User(username=request.form['username'], password=hashedPwd) # create user
        db.session.add(user)
        db.session.commit() # save new user in User table

        new_user = User.query.filter_by(username=request.form['username']).first() # new profile
        user_profile = Profile(user_id=new_user.id, name="no-name", surname="no-surname", avatar="saitama-batman.jpg", description="no-description", skills="no-skills,")
        db.session.add(user_profile)
        db.session.commit() # save new profile in Profile table

        return render_template('registration_success.html', username=request.form['username'])
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    username = loggedIn(session, LoggedIn)
    if username != False:
        return render_template('index.html', username=username)

    form = LoginForm()
    if form.validate_on_submit():
        pwd = request.form['password']
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if not existing_user:
            error = 'Username or password are incorrect.'
            return render_template('login.html', form=form, loggedInError=error)

        hash1 = hashpw(str(pwd).encode('utf-8'), str(existing_user.password).encode('utf-8'))
        hash2 = existing_user.password
        if hash1 != hash2:
            error = 'Username or password are incorrect.'
            return render_template('login.html', form=form, loggedInError=error)

        rand_ID = str(randId())
        while True:
            user = LoggedIn.query.filter_by(rand_id=rand_ID).first()
            if user:
                rand_ID = str(randId())
            else:
                break

        userLoggedIn = LoggedIn(username=request.form['username'], rand_id=rand_ID)
        db.session.add(userLoggedIn)
        db.session.commit()
        session['user'] = rand_ID
        return render_template('index.html', username=userLoggedIn.username)
    return render_template('login.html', form=form)



@app.route('/logout', methods=['GET'])
def logout():
    if not 'user' in session:
        form = LoginForm()
        return render_template('login.html', form=form)

    logoutUser(session=session, LoggedIn=LoggedIn, db=db)
    form = LoginForm()
    return render_template('login.html', form=form)
