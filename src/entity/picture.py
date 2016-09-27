from src import db

class Picture(db.Model):
    img_id=db.Column(db.Integer, primary_key=True)
    tooth_id=db.Column(db.Integer)
    path=db.Column(db.String(100))
    picture_type = db.Column(db.Integer)



    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit



