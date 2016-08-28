from src import db

class Tooth_location(db.Model):
    tooth_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    is_fill_tooth = db.Column(db.Boolean)
    tooth_location = db.Column(db.String(50))
    symptom = db.Column(db.String(50))
    time_of_occurrence = db.Column(db.String(50))
    step = db.Column(db.Integer)

    #def __init__(self, name):
        #self.name = name

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
