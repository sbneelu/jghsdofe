from jghsdofe import create_app, db
from jghsdofe.models import User
import sys

app = create_app()


def delete_user(username, app):

    with app.app_context():
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            print('ERROR: User not found.')
            sys.exit()

        db.session.delete(user)
        db.session.commit()

        return True





script, username = sys.argv

if delete_user(username, app):
    print('Deleted user ' + username)
    
else:
    print('An error occured.')
