from src import db

class Personal_history(db.Model):
    case_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    consumption_of_sweet = db.Column(db.String(50))
    frequency_of_sweet = db.Column(db.String(50))
    frequency_of_meal = db.Column(db.String(50))
    is_carbonic_acid = db.Column(db.String(50))
    is_floss = db.Column(db.String(50))
    times_of_teeth_brush = db.Column(db.String(50))
    time_of_teeth_brush = db.Column(db.String(50))
    long_of_teeth_brush = db.Column(db.String(50))
    electric_tooth_brush = db.Column(db.String(50))
    is_fluorine = db.Column(db.String(50))
    is_cavity_examination = db.Column(db.String(50))
    is_periodontal_treatment = db.Column(db.String(50))
    sjogren_syndrome = db.Column(db.String(50))
    salivary_gland_disease = db.Column(db.String(50))
    consciously_reduce_salivary_flow = db.Column(db.String(50))

    development_of_the_situation = db.Column(db.String(50))
    radiation_therapy_history = db.Column(db.String(50))
    loss_caries_index_up = db.Column(db.String(50))
    loss_caries_surface_index_up = db.Column(db.String(50))
    orthodontic = db.Column(db.String(50))
    additional = db.Column(db.String(50))


    def __repr__(self):
        return '<id %r>' % self.user_id
    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit