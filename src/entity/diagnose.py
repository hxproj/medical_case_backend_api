from src import db

class Diagnose(db.Model):
    tooth_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    caries_type = db.Column(db.String(20))
    caries_degree = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit

