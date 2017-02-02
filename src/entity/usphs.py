from src import db

class Usphs(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    color = db.Column(db.String(50))
    marginal_accuracy = db.Column(db.String(50))
    anatomic_form = db.Column(db.String(50))
    edge_color = db.Column(db.String(50))
    secondary_caries = db.Column(db.String(50))
    level = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit