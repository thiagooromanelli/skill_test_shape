import unittest
from unittest.mock import patch, Mock
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import StaleDataError

from app import create_app
from api.models.operation_orders import OperationOrder
from api.models.vessel_equipments import VesselEquipment


class AppTestEquipmentsEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.tester = self.app.test_client()

    def test_patch_equipment_status(self):
        uri = '/api/equipments/status'
        with patch('database.database.db.session.bulk_update_mappings'):
            with patch('database.database.db.session.commit'):
                response = self.tester.patch(uri, json=[{
                    "code": "5310B9D1",
                    "status": "inactive"
                }])
                self.assertEqual(response.status_code, 200)
            with patch('database.database.db.session.commit') as mock_commit:
                mock_commit.side_effect = StaleDataError()
                response = self.tester.patch(uri, json=[{
                    "code": "5310B9D1",
                    "status": "inactive"
                }])
                self.assertEqual(response.status_code, 400)
                mock_commit.side_effect = DataError(orig="Data error", params=None, statement=None)
                response = self.tester.patch(uri, json=[{
                    "code": "5310B9D1",
                    "status": "inactive"
                }])
                self.assertEqual(response.status_code, 400)

    def test_get_operation_orders(self):
        uri = '/api/equipments/orders'
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock_get_sqlalchemy = mock.return_value = Mock()
            mock_get_sqlalchemy.all.return_value = [
                OperationOrder(equipment_code="12345", operation_type="clean", operation_cost=1000),
                OperationOrder(equipment_code="67890", operation_type="replace", operation_cost=1234)
            ]
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.get_json(), dict))
            self.assertEqual(response.get_json()["count"], 2)

    def test_post_operation_orders(self):
        uri = '/api/equipments/orders'
        with patch('database.database.db.session.add'):
            with patch('database.database.db.session.commit'):
                response = self.tester.post(uri, json={
                  "code": "123456",
                  "cost": 1000,
                  "type": "clean"
                })
                self.assertEqual(response.status_code, 201)
                response = self.tester.post(uri, data={
                    "code": "123456",
                    "cost": 1000,
                    "type": "clean"
                })
                self.assertEqual(response.status_code, 400)
            with patch('database.database.db.session.commit') as mock_commit:
                mock_commit.side_effect = IntegrityError(params=None, orig="Error Test", statement=None)
                response = self.tester.post(uri, json={
                    "code": "123456",
                    "cost": 1000,
                    "type": "clean"
                })
                self.assertEqual(response.status_code, 400)

    def test_get_operation_orders_with_code(self):
        uri = '/api/equipments/12345/orders'
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock.return_value.filter.return_value.first.return_value = OperationOrder(
                equipment_code="12345",
                operation_type="clean",
                operation_cost=1000
            )
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.get_json(), dict))

    def test_get_total_cost(self):
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock.return_value.filter.return_value = [
                OperationOrder(
                    equipment_code="12345",
                    operation_type="clean",
                    operation_cost=1000
                ),
                OperationOrder(
                    equipment_code="12345",
                    operation_type="clean",
                    operation_cost=1000
                )
            ]
            uri = '/api/equipments/orders/total-cost'
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 400)

        with patch('database.database.db.session') as mock_count:
            mock_count.query.return_value.join.return_value.filter.return_value.count.return_value = 2
            uri = '/api/equipments/orders/total-cost?code=12345'
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 200)

    def test_get_avg_cost(self):
        with patch('database.database.db.session') as mock_count:
            mock_count.query.return_value.join.return_value.filter.return_value.count.return_value = 2
            uri = '/api/equipments/orders/avg-cost'
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 400)
            uri = '/api/equipments/orders/avg-cost?code=MV100'
            response = self.tester.get(uri)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
