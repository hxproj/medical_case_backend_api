from src import db

class Prognosis_of_management(db.Model):
    tooth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    patient_type = db.Column(db.Integer)