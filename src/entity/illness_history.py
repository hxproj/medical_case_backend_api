from src import db

class Illness_history(db.Model):
    tooth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    is_primary = db.Column(db.Boolean)
    is_very_bad = db.Column(db.String(50))
    is_night_pain_self_pain = db.Column(db.String(50))
    medicine_name = db.Column(db.String(50))
    is_relief = db.Column(db.String(50))
    fill_type = db.Column(db.String(50))
    is_hypnalgia = db.Column(db.String(50))
    is_sensitive_cold_heat = db.Column(db.String(50))
    is_cold_hot_stimulationpain = db.Column(db.String(50))
    is_delayed_pain = db.Column(db.String(50))
    cure_time = db.Column(db.String(50))
    fill_state = db.Column(db.String(50))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit