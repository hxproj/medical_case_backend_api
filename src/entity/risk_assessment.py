from src import db

class Risk_assessment(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tooth_id = db.Column(db.Integer)
    fluorine_protection = db.Column(db.String(50))
    sugary_foods = db.Column(db.String(50))
    relative_illness = db.Column(db.String(50))
    need_record = db.Column(db.String(50))
    alcohol_drugs = db.Column(db.String(50))
    radiotherapy = db.Column(db.String(50))
    eating_disorders = db.Column(db.String(50))
    saliva_medicine = db.Column(db.String(50))
    special_care = db.Column(db.String(50))
    caries_lost = db.Column(db.String(50))
    soft_dirt = db.Column(db.String(50))
    special_tooth_shape = db.Column(db.String(50))
    adjacent_caries = db.Column(db.String(50))
    tooth_exposure = db.Column(db.String(50))
    fill_overhang = db.Column(db.String(50))
    appliance = db.Column(db.String(50))
    dry_syndrome = db.Column(db.String(50))
    hole = db.Column(db.String(50))
    risk_level = db.Column(db.Integer)


    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit

    def calculate_risk(self):
        level1 = 0
        level2 = 0
        level3 = 0
