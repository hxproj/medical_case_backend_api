from src import db


class Surgical(db.Model):
    tooth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(20))
    anesthesia_medicine = db.Column(db.String(20))
    part_anesthesia = db.Column(db.String(20))
    rubber = db.Column(db.String(20))
    tools = db.Column(db.String(20))
    shape_of_hole = db.Column(db.String(20))
    depth_of_hole = db.Column(db.String(20))
    is_piece = db.Column(db.String(20))
    is_chock = db.Column(db.String(20))
    shade_guide = db.Column(db.String(100))
    color_of_tooth = db.Column(db.String(20))
    disinfect = db.Column(db.String(20))
    bottom = db.Column(db.String(20))
    full_etching = db.Column(db.String(100))
    self_etching = db.Column(db.String(100))
    coating_time = db.Column(db.String(20))
    illumination_time = db.Column(db.String(20))
    resin = db.Column(db.String(20))
    modification = db.Column(db.String(20))
    lamp = db.Column(db.String(20))
    time_of_lamp = db.Column(db.String(20))
    polishing = db.Column(db.String(20))
    appease_medicine = db.Column(db.String(20))
    observed_time = db.Column(db.String(20))
    modulo = db.Column(db.String(20))
    inlay = db.Column(db.String(20))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
