from src import db


class Surgical(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    tooth_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    handle_type = db.Column(db.Integer)
    specific_method = db.Column(db.String(100))
    anesthesia_medicine = db.Column(db.String(100))
    part_anesthesia = db.Column(db.String(100))
    rubber = db.Column(db.String(100))
    microscope = db.Column(db.String(100))
    tools = db.Column(db.String(100))
    shape_of_hole = db.Column(db.String(100))
    depth_of_hole = db.Column(db.String(100))
    is_piece = db.Column(db.String(100))
    is_chock = db.Column(db.String(100))
    shade_guide = db.Column(db.String(100))
    color_of_tooth = db.Column(db.String(100))
    disinfect = db.Column(db.String(100))
    bottom = db.Column(db.String(100))
    etching_type = db.Column(db.String(100))
    full_etching = db.Column(db.String(100))
    self_etching = db.Column(db.String(100))
    coating_time = db.Column(db.String(100))
    illumination_time = db.Column(db.String(100))
    resin = db.Column(db.String(100))
    color_of_resin = db.Column(db.String(100))
    modification = db.Column(db.String(100))
    lamp = db.Column(db.String(100))
    time_of_lamp = db.Column(db.String(100))
    appease_medicine = db.Column(db.String(100))
    observed_time = db.Column(db.String(100))
    modulo = db.Column(db.String(100))
    inlay = db.Column(db.String(100))
    compromise = db.Column(db.String(100))
    polishing = db.Column(db.String(100))
    drill_needle = db.Column(db.String(100))
    gingival_retraction = db.Column(db.String(100))
    additional = db.Column(db.String(300))
    compromise_polishing_additional =  db.Column(db.String(300))


    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit