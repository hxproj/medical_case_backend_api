from src import db


class PastHistory(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    systemillness = db.Column(db.String(300))
    infectiousdisease = db.Column(db.String(300))
    dragallergy = db.Column(db.String(300))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit