from src import db

class Difficulty_assessment(db.Model):
    tooth_id  = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    tooth_surface_and_location = db.Column(db.String(20))
    caries_depth = db.Column(db.String(20))
    technology_type = db.Column(db.String(20))
    history_of_fill = db.Column(db.String(20))
    mouth_opening = db.Column(db.String(20))
    gag_reflex = db.Column(db.String(20))
    saliva = db.Column(db.String(20))
    dental_phobia = db.Column(db.String(20))
    difficulty_rating = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit


