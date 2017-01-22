from src import db

class Illness_case(db.Model):
    case_id = db.Column(db.Integer,primary_key=True)
    tooth_id = db.Column(db.Integer)
    case_type = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    if_handle = db.Column(db.Integer)
    step = db.Column(db.String(50))
    judge_doctor = db.Column(db.String(50))

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        if dit['date']:
            dit['date'] = dit['date'].strftime('%Y-%m-%d ')
        tooth_step_list = dit['step'].split(',')
        if '' in tooth_step_list:
            tooth_step_list.remove('')
        num_list = []
        for i in range(len(tooth_step_list)):
            num_list.append((int)(tooth_step_list[i]))
        dit['step'] = num_list
        return dit