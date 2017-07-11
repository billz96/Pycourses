from uuid import uuid4

def randId():
    return uuid4().hex

def loggedIn(session, LoggedIn):
    if ('user' in session) and (session['user'] is not None):
        userLoggedIn = LoggedIn.query.filter_by(rand_id=str(session['user'])).first()
        if userLoggedIn:
            return userLoggedIn.username
        return False
    else:
        return False

def logoutUser(session, LoggedIn, db):
    randID = session['user']
    user = LoggedIn.query.filter_by(rand_id=str(randID).encode('utf-8')).delete()
    session.pop('user', None)
