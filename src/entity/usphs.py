from src import db

class Usphs(db.Model):
    tooth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    color = db.Column(db.String(50))
    marginal_accuracy = db.Column(db.String(50))
    anatomic_form = db.Column(db.String(50))
    surfaceness = db.Column(db.String(20))
    edge_color = db.Column(db.String(20))
    occlusal_contact = db.Column(db.String(20)) # yao he jie chu
    sensitivity_of_tooth = db.Column(db.String(100))# ya chi min gan
    secondary_caries = db.Column(db.String(20))
    integrity = db.Column(db.String(20))
    level = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
