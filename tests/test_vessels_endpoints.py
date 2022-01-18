import unittest
from unittest.mock import patch, Mock

from sqlalchemy.exc import IntegrityError

from app import create_app
from api.models.vessels import Vessel
from api.models.vessel_equipments import VesselEquipment


class AppTestVesselsEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.tester = self.app.test_client()

    def test_get_vessels(self):
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock_get_sqlalchemy = mock.return_value = Mock()
            mock_get_sqlalchemy.all.return_value = [
                Vessel(code="MV100"),
                Vessel(code="MV101")
            ]
            response = self.tester.get('/api/vessels')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.get_json(), dict))
            self.assertEqual(response.get_json(), {
              "count": 2,
              "vessels": [
                {
                  "code": "MV100"
                },
                {
                  "code": "MV101"
                }
              ]
            })

    def test_post_vessels(self):
        with patch('database.database.db.session.add'):
            with patch('database.database.db.session.commit'):
                response = self.tester.post('/api/vessels', json={"code": "MV100"})
                self.assertEqual(response.status_code, 201)
                response = self.tester.post('/api/vessels', data={"code": "MV100"})
                self.assertEqual(response.status_code, 400)
            with patch('database.database.db.session.commit') as mock_commit:
                mock_commit.side_effect = IntegrityError(params=None, orig="Error Test", statement=None)
                response = self.tester.post('/api/vessels', json={"code": "MV100"})
                self.assertEqual(response.status_code, 400)

    def test_get_vessels_with_code(self):
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock.return_value.filter.return_value.first.return_value = Vessel(code="MV100")
            response = self.tester.get('/api/vessels/MV100')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.get_json(), dict))
            self.assertEqual(response.get_json(), {
              "code": "MV100"
            })

    def test_post_vessels_equipments(self):
        uri = '/api/vessels/MV100/equipments'
        with patch('database.database.db.session.add'):
            with patch('database.database.db.session.commit'):
                response = self.tester.post(uri, json={
                  "code": "5310B9D1",
                  "location": "Brazil",
                  "name": "cleaner"
                })
                self.assertEqual(response.status_code, 201)
                response = self.tester.post(uri, data={
                  "code": "5310B9D1",
                  "location": "Brazil",
                  "name": "cleaner"
                })
                self.assertEqual(response.status_code, 400)
            with patch('database.database.db.session.commit') as mock_commit:
                mock_commit.side_effect = IntegrityError(params=None, orig="Error Test", statement=None)
                response = self.tester.post(uri, json={
                  "code": "5310B9D1",
                  "location": "Brazil",
                  "name": "cleaner"
                })
                self.assertEqual(response.status_code, 400)

    def test_get_vessels_equipments(self):
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock.return_value.filter.return_value = [
                VesselEquipment(
                    code="5310B9D1",
                    vessel_code="MV100",
                    location="Brazil",
                    name="shooter",
                    equip_status="active"
                ),
                VesselEquipment(
                    code="5310B9D2",
                    vessel_code="MV100",
                    location="Brazil",
                    name="cleaner",
                    equip_status="inactive"
                )
            ]
            response = self.tester.get('/api/vessels/MV100/equipments')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {
                'count': 2,
                'equipments': [{
                    'code': '5310B9D1',
                    'location': 'Brazil',
                    'name': 'shooter',
                    'status': 'active'
                }, {
                    'code': '5310B9D2',
                    'location': 'Brazil',
                    'name': 'cleaner',
                    'status': 'inactive'
                }]})

    def test_get_vessels_equipments_with_code(self):
        with patch('flask_sqlalchemy._QueryProperty.__get__') as mock:
            mock.return_value.filter.return_value.first.return_value = VesselEquipment(
                code="5310B9D1",
                vessel_code="MV100",
                location="Brazil",
                name="shooter",
                equip_status="active"
            )
            response = self.tester.get('/api/vessels/MV100/equipments/5310B9D1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {
                'code': '5310B9D1',
                'location': 'Brazil',
                'name': 'shooter',
                'status': 'active'
            })


if __name__ == '__main__':
    unittest.main()
