from sqlalchemy.exc import OperationalError
from src import db
def create_db():
    try:
        db.create_all()
    except OperationalError as e:
        if e.orig.args[0] == 1045:
            print 'wrong password.'
        elif e.orig.args[0] == 2003:
            print 'can not connect to the database, please check IP address and port, and check if the database is opened.'
        elif e.orig.args[0] == 1049:
            print 'the database isn\'t exist, please create database schema first.'
        return False
    return True

result = create_db()
if result:
    print('Successfully created tables.')