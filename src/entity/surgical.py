from src import db


class Surgical(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(200))
    anesthesia_medicine = db.Column(db.String(200))
    part_anesthesia = db.Column(db.String(200))
    rubber = db.Column(db.String(200))
    microscope = db.Column(db.String(200))
    tools = db.Column(db.String(200))
    shape_of_hole = db.Column(db.String(200))
    depth_of_hole = db.Column(db.String(200))
    is_piece = db.Column(db.String(200))
    is_chock = db.Column(db.String(200))
    shade_guide = db.Column(db.String(200))
    color_of_tooth = db.Column(db.String(200))
    disinfect = db.Column(db.String(200))
    bottom = db.Column(db.String(200))
    etching_type = db.Column(db.String(200))
    full_etching = db.Column(db.String(200))
    self_etching = db.Column(db.String(200))
    coating_time = db.Column(db.String(200))
    illumination_time = db.Column(db.String(200))
    resin = db.Column(db.String(200))
    color_of_resin = db.Column(db.String(200))
    modification = db.Column(db.String(200))
    lamp = db.Column(db.String(200))
    time_of_lamp = db.Column(db.String(200))
    polishing = db.Column(db.String(200))
    appease_medicine = db.Column(db.String(200))
    observed_time = db.Column(db.String(200))
    modulo = db.Column(db.String(200))
    inlay = db.Column(db.String(200))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
