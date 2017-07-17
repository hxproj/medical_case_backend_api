from src import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    id_number = db.Column(db.String(20))
    gender = db.Column(db.Boolean)
    occupation = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    birthday = db.Column(db.Integer)
    main_doctor = db.Column(db.String(50))
    in_date = db.Column(db.DateTime)

    #def __init__(self, name):
        #self.name = name

    def __repr__(self):
        return '<user %r>' % self.name
    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        if dit['in_date']:
            dit['in_date']= dit['in_date'].strftime('%Y-%m-%d %H:%M:%S')
        return dit