from jghsdofe import create_app, db
from jghsdofe.models import User
import sys

app = create_app()


def give_permission(username, level, app):

    with app.app_context():
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            print('ERROR: User not found.')
            sys.exit()

        if level == 'bronze':
            user.bronze_access = True

        elif level == 'silver':
            user.silver_access = True

        elif level == 'gold':
            user.gold_access = True

        elif level == 'admin':
            user.is_admin = True

        else:
            print('ERROR: Invalid level.')
            sys.exit()

        db.session.commit()

        return {
            "username": user.username,
            "bronze_access": str(user.bronze_access),
            "silver_access": str(user.silver_access),
            "gold_access": str(user.gold_access),
            "is_admin": str(user.is_admin)
        }


def remove_permission(username, level, app):

    with app.app_context():
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            print('ERROR: User not found.')
            sys.exit()

        if level == 'bronze':
            user.bronze_access = False

        elif level == 'silver':
            user.silver_access = False

        elif level == 'gold':
            user.gold_access = False

        elif level == 'admin':
            user.is_admin = False

        else:
            print('ERROR: Invalid level.')
            sys.exit()

        db.session.commit()

        return {
            "username": user.username,
            "bronze_access": str(user.bronze_access),
            "silver_access": str(user.silver_access),
            "gold_access": str(user.gold_access),
            "is_admin": str(user.is_admin)
        }



def check_permission(username, app):

    with app.app_context():
        user = User.query.filter_by(username=username.lower()).first()
        if not user:
            print('ERROR: User not found.')
            sys.exit()

        return {
            "username": user.username,
            "bronze_access": str(user.bronze_access),
            "silver_access": str(user.silver_access),
            "gold_access": str(user.gold_access),
            "is_admin": str(user.is_admin)
        }


script, username, fn = sys.argv

user = None

if fn == 'give':
    level = input('Level: ')
    user = give_permission(username.lower(), level.lower(), app)

elif fn == 'remove':
    level = input('Level: ')
    user = remove_permission(username.lower(), level.lower(), app)

elif fn == 'check':
    user = check_permission(username.lower(), app)

else:
    print('ERROR: Invalid function.')
    sys.exit()

print('USERNAME: ' + user['username'])
print('BRONZE ACCESS: ' + user['bronze_access'])
print('SILVER ACCESS: ' + user['silver_access'])
print('GOLD ACCESS: ' + user['gold_access'])
print('ADMIN: ' + user['is_admin'])
