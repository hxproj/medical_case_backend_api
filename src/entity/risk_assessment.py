from src import db

class Risk_assessment(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    early_carie = db.Column(db.String(50))
    can_see =db.Column(db.String(50))
    lost_tooth = db.Column(db.String(50))
    system_illness = db.Column(db.String(50))
    illness_name = db.Column(db.String(50))
    times_of_carbohydrate = db.Column(db.String(50))
    consumption_of_carbohydrate = db.Column(db.String(50))
    times_of_meal = db.Column(db.String(50))
    speed_of_saliva = db.Column(db.String(50))
    ablity_saliva = db.Column(db.String(50))
    bacteria = db.Column(db.String(50))
    consumption =db.Column(db.String(50))
    fluorine_with_water = db.Column(db.String(50))
    fluorine = db.Column(db.String(50))
    seal = db.Column(db.String(50))
    times_of_tooth_brush = db.Column(db.String(50))
    long_of_tooth_brush = db.Column(db.String(50))
    health_care = db.Column(db.String(50))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit