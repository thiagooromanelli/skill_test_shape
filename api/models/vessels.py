from database.database import db


class Vessel(db.Model):
    __tablename__ = 'vessels'
    __table_args__ = {'extend_existing': True}

    code = db.Column(db.String, primary_key=True)
    vessels_equipment = db.relationship('VesselEquipment', cascade='all,delete', backref='vessels')

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return f"<Vessel {self.code}>"
