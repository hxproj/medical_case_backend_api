from src import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    occupation = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    in_date = db.Column(db.DateTime)

    #def __init__(self, name):
        #self.name = name

    def __repr__(self):
        return '<user %r>' % self.name
    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        dit['in_date']= dit['in_date'].strftime('%Y-%m-%d %H:%M:%S')
        return dit