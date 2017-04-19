from src import db


class Non_surgical(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(50))
    fluorination = db.Column(db.String(50))
    silver_nitrate = db.Column(db.String(50))
    additional_device = db.Column(db.String(50))
    reagent = db.Column(db.String(50))
    non_surgical_tools = db.Column(db.String(50))
    non_surgical_lamp = db.Column(db.String(50))
    check_time = db.Column(db.String(50))
    time_of_etching = db.Column(db.String(50))
    non_surgical_coating_time = db.Column(db.String(50))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit