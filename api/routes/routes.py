from flask import request, jsonify, Blueprint
from flask_api import status

from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import and_
from sqlalchemy.orm.exc import StaleDataError

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
@api.route('/vessels/<vessel_code>', methods=['GET'])
def handle_vessels(vessel_code=None):
    # Handle POST requests
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
        return ERROR_RESP_JSON_FORMAT, status.HTTP_400_BAD_REQUEST
    # Handle GET requests
    # If not optional parameter
    if vessel_code is None:
        try:
            vessels = Vessel.query.all()
            results = [{"code": vessel.code} for vessel in vessels]
            return jsonify({"count": len(results), "vessels": results}), status.HTTP_200_OK
        except Exception as err:
            return jsonify({"error": f"{err}"}), status.HTTP_500_INTERNAL_SERVER_ERROR
    # Otherwise use the parameter
    try:
        vessel = Vessel.query.filter(Vessel.code == vessel_code).first()
        if vessel is not None:
            return jsonify({"code": vessel.code}), status.HTTP_200_OK
        return jsonify({"message": f"Vessel '{vessel_code}' not found."}), status.HTTP_404_NOT_FOUND
    except Exception as err:
        return jsonify({"error": f"{err}"}), status.HTTP_500_INTERNAL_SERVER_ERROR


@api.route('/vessels/<vessel_code>/equipments', methods=['POST', 'GET'])
@api.route('/vessels/<vessel_code>/equipments/<equipment_code>', methods=['GET'])
def handle_vessels_equipments(vessel_code, equipment_code=None):
    # Handle POST requests
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
    # Handle GET requests
    # Return all equipments in a vessel (filter status is optional)
    if equipment_code is None:
        equipment_status = request.args.get("status", None)
        if equipment_status:
            equipments = VesselEquipment.query.filter(and_(
                VesselEquipment.vessel_code == vessel_code,
                VesselEquipment.status == equipment_status
            ))
        else:
            equipments = VesselEquipment.query.filter(
                VesselEquipment.vessel_code == vessel_code
            )
        results = [{
            "code": equipment.code,
            "name": equipment.name,
            "location": equipment.location,
            "status": equipment.status
        } for equipment in equipments]
        return jsonify({"count": len(results), "equipments": results}), status.HTTP_200_OK
    # Return equipment with given equipment_code
    try:
        equipment = VesselEquipment.query.filter(and_(
            VesselEquipment.vessel_code == vessel_code,
            VesselEquipment.code == equipment_code
        )).first()
        if equipment is not None:
            return jsonify({
                "code": equipment.code,
                "name": equipment.name,
                "location": equipment.location,
                "status": equipment.status
            }), status.HTTP_200_OK
        return jsonify({"message": f"Equipment '{equipment_code}' not found."}), status.HTTP_404_NOT_FOUND
    except Exception as err:
        return jsonify({"error": f"{err}"}), status.HTTP_500_INTERNAL_SERVER_ERROR


@api.route('/equipments/status', methods=['PATCH'])
def update_equipment_status():
    data = request.get_json()
    try:
        db.session.bulk_update_mappings(
            VesselEquipment,
            data
        )
        db.session.commit()
        return jsonify({"message": "Status updated!"}), 200
    except StaleDataError as err:
        db.session.rollback()
        print(type(err))
        return jsonify({"error": "Invalid code were passed. Check input."}), status.HTTP_400_BAD_REQUEST
    except DataError as err:
        db.session.rollback()
        print(type(err))
        return jsonify({"error": "Invalid input value. Check values."}), status.HTTP_400_BAD_REQUEST


@api.route('/equipments/orders', methods=['POST', 'GET'])
@api.route('/equipments/<equipment_code>/orders', methods=['GET'])
def operation_orders(equipment_code=None):
    # Handle POST requests
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
    # Handle GET requests
    # Return all operation orders
    if equipment_code is None:
        orders = OperationOrder.query.all()
        results = [{
            "id": order.id,
            "code": order.equipment_code,
            "type": order.type,
            "cost": order.cost
        } for order in orders]
        return jsonify({"count": len(results), "orders": results}), status.HTTP_200_OK
    # Return all operation orders related to equipment_code given
    try:
        orders = OperationOrder.query.filter(
            OperationOrder.equipment_code == equipment_code
        )
        results = [{
            "id": order.id,
            "code": order.equipment_code,
            "type": order.type,
            "cost": order.cost
        } for order in orders]
        return jsonify({"count": len(results), "orders": results}), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"error": f"{err}"}), status.HTTP_500_INTERNAL_SERVER_ERROR


@api.route('/equipments/orders/total-cost', methods=['GET'])
def total_cost_by_equipment():
    total_cost = 0
    orders_list = []
    equipment_code = request.args.get("code", None)
    equipment_name = request.args.get("name", None)

    if equipment_code:
        try:
            orders = OperationOrder.query.filter(OperationOrder.equipment_code == equipment_code)
            for order in orders:
                orders_list.append(order.id)
                total_cost += order.cost
            return jsonify({
                "orders": orders_list,
                "total-cost": total_cost
            }), status.HTTP_200_OK
        except Exception as err:
            return jsonify({"error": f"{err}"}), status.HTTP_400_BAD_REQUEST
    elif equipment_name:
        try:
            data = db.session.query(
                OperationOrder,
                VesselEquipment
            ).join(VesselEquipment).filter(VesselEquipment.name == equipment_name)
            if len(data.all()) == 0:
                return jsonify({"error": "No orders were found for this equipment"}), status.HTTP_404_NOT_FOUND
            for order, equipment in data:
                orders_list.append(order.id)
                total_cost += order.cost
            return jsonify({
                "orders": orders_list,
                "total-cost": total_cost
            }), status.HTTP_200_OK
        except Exception as err:
            return jsonify({"error": f"{err}"}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({
            "error": "No filters were passed. Try to filter by 'code' or 'name'"
        }), status.HTTP_400_BAD_REQUEST


@api.route('/equipments/orders/avg-cost', methods=['GET'])
def avg_cost_by_vessel():
    total_cost = 0
    vessel_code = request.args.get("code", None)
    if vessel_code:
        try:
            data = db.session.query(
                OperationOrder,
                VesselEquipment
            ).join(VesselEquipment).filter(VesselEquipment.vessel_code == vessel_code)
            if len(data.all()) == 0:
                return jsonify({"error": "No orders were found for this vessel"}), status.HTTP_404_NOT_FOUND
            for order, equipment in data:
                total_cost += order.cost
            avg_cost = total_cost/len(data.all())
            return jsonify({
                "code": vessel_code,
                "avg-cost": avg_cost
            }), status.HTTP_200_OK
        except Exception as err:
            return jsonify({"error": f"{err}"}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({
            "error": "No filters were passed. Try to filter by 'code'"
        }), status.HTTP_400_BAD_REQUEST
