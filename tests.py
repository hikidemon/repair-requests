import unittest
from app import app, db
from models import User, RepairRequest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
           
            user = User(username='testuser', password='password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_user(self):
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_create_request(self):
        response = self.app.post('/requests', json={
            'date_added': '2023-10-21T12:00:00', 
            'problem_description': 'Test problem',
            'status': 'not completed',
            'responsible_person': 'testuser'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_requests(self):
        self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password'
        })
        response = self.app.get('/requests')
        self.assertEqual(response.status_code, 200)

    def test_update_request(self):
        self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password'
        })
        request = RepairRequest(description='Old problem', status='not completed', responsible_person='testuser')
        db.session.add(request)
        db.session.commit()
        
        response = self.app.put(f'/requests/{request.id}', json={
            'status': 'completed',
            'problem_description': 'Updated problem'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password'
        })
        request = RepairRequest(description='Delete me', status='not completed', responsible_person='testuser')
        db.session.add(request)
        db.session.commit()
        
        response = self.app.delete(f'/requests/{request.id}')
        self.assertEqual(response.status_code, 204)

    def test_get_statistics(self):
        self.app.post('/login', json={
            'username': 'testuser',
            'password': 'password'
        })
        response = self.app.get('/statistics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
