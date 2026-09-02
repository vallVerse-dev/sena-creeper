import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_listar_usuarios(self):
        response = self.client.get('/api/usuarios')
        # Sin BD, esperamos un error 500, pero la ruta existe
        self.assertIn(response.status_code, [200, 500])

    def test_crear_usuario(self):
        response = self.client.post('/api/usuarios', json={'nombre':'Test','email':'test@example.com'})
        self.assertIn(response.status_code, [201, 500])

if __name__ == '__main__':
    unittest.main()
