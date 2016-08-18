from src import db

class Oral_examination(db.Model):
    tooth_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    tooth_location = db.Column(db.String(20))
    caries_tired = db.Column(db.String(20))
    depth = db.Column(db.String(20))
    fill = db.Column(db.String(20))
    secondary = db.Column(db.String(20))
    color_of_caries = db.Column(db.String(20))
    flex_of_caries = db.Column(db.String(20))
    cold = db.Column(db.Integer)
    hot = db.Column(db.Integer)
    touch = db.Column(db.Integer)
    bite = db.Column(db.Integer)
    vitality_value_of_teeth = db.Column(db.Integer)
    gingival_hyperemia = db.Column(db.String(20))
    tartar_up = db.Column(db.String(20))
    tartar_down = db.Column(db.String(20))
    bop = db.Column(db.String(20))
    periodontal_pocket_depth = db.Column(db.String(20))
    furcation = db.Column(db.String(20))
    location = db.Column(db.String(20))
    fistula = db.Column(db.String(20))
    overflow_pus = db.Column(db.String(20))
    mobility = db.Column(db.String(20))
    loss_caries_index_up = db.Column(db.Integer)
    development_of_the_situation = db.Column(db.String(20))
    relations_between_teeth = db.Column(db.String(20))
    is_teeth_crowd = db.Column(db.String(20))
    involution_teeth = db.Column(db.String(20))
    tooth_shape = db.Column(db.String(20))
    treatment = db.Column(db.String(20))
    orthodontic = db.Column(db.String(20))
    X_Ray_location = db.Column(db.String(20))
    X_Ray_depth = db.Column(db.String(20))
    X_Ray_fill_quality = db.Column(db.String(20))
    CT_shows = db.Column(db.String(300))
    piece = db.Column(db.String(300))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit


