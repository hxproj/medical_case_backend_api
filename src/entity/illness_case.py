from src import db

class Illness_case(db.Model):
    case_id = db.Column(db.Integer,primary_key=True)
    tooth_id = db.Column(db.Integer)
    case_type = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    if_handle = db.Column(db.Integer)

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        if dit['in_date']:
            dit['in_date'] = dit['in_date'].strftime('%Y-%m-%d %H:%M:%S')
        return dit