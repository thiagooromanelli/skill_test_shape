from flask import request, jsonify, Blueprint
from flask_api import status

from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from database.database import db

from api.models.operation_orders import OperationOrder
from api.models.vessels import Vessel
from api.models.vessel_equipments import VesselEquipment


api = Blueprint('api', __name__)
ERROR_RESP_JSON_FORMAT = {"error": "The request payload is not in JSON format"}


@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "PONG"}), status.HTTP_200_OK


@api.route('/vessels', methods=['POST', 'GET'])
def handle_vessels():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_vessel = Vessel(code=data['code'])
            try:
                db.session.add(new_vessel)
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                return jsonify({
                           "error": f"{err.orig}"
                       }), status.HTTP_400_BAD_REQUEST
            return jsonify({
                       "message": f"Vessel '{new_vessel.code}' has been successfully created."
                   }), status.HTTP_201_CREATED
        else:
            return ERROR_RESP_JSON_FORMAT, status.HTTP_400_BAD_REQUEST
    else:
        vessels = Vessel.query.all()
        results = [{"code": vessel.code} for vessel in vessels]
        return jsonify({"count": len(results), "vessels": results}), status.HTTP_200_OK


@api.route('/vessels/<vessel_code>/equipments', methods=['POST', 'GET'])
def handle_vessels_equipment(vessel_code):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_equipment = VesselEquipment(
                code=data['code'],
                vessel_code=vessel_code,
                name=data['name'],
                location=data['location']
            )
            try:
                db.session.add(new_equipment)
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                return jsonify({
                           "error": f"{err.orig}"
                       }), status.HTTP_400_BAD_REQUEST
            return jsonify({
                       "message": f"Equipment '{new_equipment.code}' has been successfully created."
                   }), status.HTTP_201_CREATED
        else:
            return ERROR_RESP_JSON_FORMAT, status.HTTP_400_BAD_REQUEST
    else:
        equipments = VesselEquipment.query.filter(and_(
            VesselEquipment.vessel_code == vessel_code, VesselEquipment.status == "active"
        ))
        results = [{
            "code": equipment.code,
            "vessel_code": equipment.vessel_code,
            "name": equipment.name,
            "location": equipment.location,
            "status": equipment.status
        } for equipment in equipments]
        return jsonify({"count": len(results), "equipments": results}), status.HTTP_200_OK


@api.route('/vessels/<vessel_code>/equipments/<equipment_code>', methods=['PATCH'])
def patch_equipment(vessel_code, equipment_code):
    if request.is_json:
        data = request.get_json()
        equipment = VesselEquipment.query.filter(
            VesselEquipment.vessel_code == vessel_code and VesselEquipment.code == equipment_code
        ).first()
        equipment.status = data['status']
        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            return jsonify({
                       "error": f"{err}"
                   }), status.HTTP_400_BAD_REQUEST
        return {}, status.HTTP_204_NO_CONTENT
    else:
        return ERROR_RESP_JSON_FORMAT, status.HTTP_400_BAD_REQUEST


@api.route('/operation_orders', methods=['POST', 'GET'])
def operation_orders():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_order = OperationOrder(
                equipment_code=data["code"],
                operation_type=data["type"],
                operation_cost=data["cost"]
            )
            try:
                db.session.add(new_order)
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                return jsonify({
                           "error": f"{err.orig}"
                       }), status.HTTP_400_BAD_REQUEST
            return jsonify({
                       "message": f"Operation order '{new_order.id}' has been successfully created."
                   }), status.HTTP_201_CREATED
        else:
            return ERROR_RESP_JSON_FORMAT, status.HTTP_400_BAD_REQUEST
    else:
        orders = OperationOrder.query.all()
        results = [{
            "id": order.id,
            "code": order.equipment_code,
            "type": order.type,
            "cost": order.cost
        } for order in orders]
        return jsonify({"count": len(results), "orders": results}), status.HTTP_200_OK


@api.route('/operation_orders/equipment/<equipment_code>', methods=['GET'])
def total_cost_by_equipment(equipment_code):
    total = 0
    try:
        orders = OperationOrder.query.filter(OperationOrder.equipment_code == equipment_code)
        for order in orders:
            total += order.cost
        return jsonify({"message": f"The total cost in operation of equipment '{equipment_code}' is {total}"}), 200
    except Exception as err:
        return jsonify({"error": f"{err}"}), 400
