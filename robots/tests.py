from django.test import TestCase, Client
from datetime import datetime
from robots.models import Robot

class RobotTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/create_robot/'
        self.valid_data = {
            "model": "R2",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
    
    def test_create_robot_success(self):
        response = self.client.post(self.url, data=self.valid_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)        

        robot = Robot.objects.last()
        self.assertEqual(robot.serial, "R2-D2")
        self.assertEqual(robot.model, "R2")
        self.assertEqual(robot.version, "D2")
        self.assertEqual(robot.created, datetime.strptime("2022-12-31 23:59:59", '%Y-%m-%d %H:%M:%S'))
    
    
    def test_create_robot_invalid_model(self):
        invalid_data = self.valid_data.copy()
        invalid_data["model"] = "R22" 
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        

    def test_create_robot_invalid_version(self):
        invalid_data = self.valid_data.copy()
        invalid_data["version"] = "D22" 
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        

    def test_create_robot_invalid_date(self):
        invalid_data = self.valid_data.copy()
        invalid_data["created"] = "2022-12-31T23:59:59" 
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)   
    
    
    def test_create_robot_missing_fields(self):
        invalid_data = {
            "model": "R2",
            "version": "D2",
        }
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        invalid_data = {
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        invalid_data = {
            "model": "R2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(self.url, data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

class ExportExcelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/export_excel/'

    def test_export_excel_response(self):
        response = self.client.get(self.url)        
    
        self.assertEqual(response.status_code, 200)        

        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        self.assertTrue('Content-Disposition' in response)