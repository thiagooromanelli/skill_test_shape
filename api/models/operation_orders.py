import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.database import db


class OperationOrder(db.Model):
    __tablename__ = 'operation_orders'
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    equipment_code = db.Column(db.String, db.ForeignKey('vessel_equipments.code'))
    type = db.Column(db.String)
    cost = db.Column(db.Integer)

    def __init__(self, equipment_code, operation_type, operation_cost):
        self.equipment_code = equipment_code
        self.type = operation_type
        self.cost = operation_cost

    def __repr__(self):
        return f"<OperationOrder {self.id}>"
