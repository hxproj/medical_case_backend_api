from src import db

class Prognosis_of_management(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tooth_id = db.Column(db.Integer)
    patient_type = db.Column(db.Integer)

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit

