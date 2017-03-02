from src import db

class Diagnose(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    caries_type = db.Column(db.String(20))
    caries_degree = db.Column(db.String(20))
    cure_plan = db.Column(db.String(50))
    specification = db.Column(db.String(50))
    additional = db.Column(db.String(300))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit

