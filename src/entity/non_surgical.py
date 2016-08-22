from src import db


class Non_surgical(db.Model):
    tooth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(20))
    fluorination = db.Column(db.String(20))
    silver_nitrate = db.Column(db.String(20))
    additional_device = db.Column(db.String(20))
    reagent = db.Column(db.String(20))
    tools = db.Column(db.String(20))
    lamp = db.Column(db.String(20))
    check_time = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
