from src import db


class Non_surgical(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(200))
    fluorination = db.Column(db.String(200))
    silver_nitrate = db.Column(db.String(200))
    additional_device = db.Column(db.String(200))
    reagent = db.Column(db.String(200))
    tools = db.Column(db.String(200))
    lamp = db.Column(db.String(200))
    check_time = db.Column(db.String(200))
    time_of_etching = db.Column(db.String(200))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
