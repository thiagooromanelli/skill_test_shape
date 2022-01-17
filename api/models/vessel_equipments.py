from database.database import db


class VesselEquipment(db.Model):
    __tablename__ = 'vessel_equipments'
    __table_args__ = {'extend_existing': True}

    code = db.Column(db.String, primary_key=True)
    vessel_code = db.Column(db.String, db.ForeignKey('vessels.code'))
    name = db.Column(db.String)
    location = db.Column(db.String)
    status = db.Column(db.Enum("active", "inactive", name="status"), default="active")

    operation_order = db.relationship('OperationOrder', cascade='all,delete', backref='vessel_equipments')

    def __init__(self, code, vessel_code, name, location, equip_status="active"):
        self.code = code
        self.vessel_code = vessel_code
        self.name = name
        self.location = location
        self.status = equip_status

    def __repr__(self):
        return f"<VesselEquipment {self.code}>"
