from src import db


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(20))
    field = db.Column(db.String(30))
    value = db.Column(db.String(200))
    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit