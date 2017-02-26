from src import db


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    name = db.Column(db.String(100))
    in_date = db.Column(db.DateTime)

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit