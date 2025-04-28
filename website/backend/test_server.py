import unittest
from io import BytesIO
from server import app

class TestServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_detect_endpoint_no_image(self):
        response = self.app.post('/detect')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No image uploaded', response.data)

    def test_detect_endpoint_with_image(self):
        with open('test_image.jpg', 'rb') as img:
            response = self.app.post('/detect', data={'image': img})
            self.assertEqual(response.status_code, 200)
            self.assertIn('scan_id', response.json)

    def test_results_endpoint_invalid_scan_id(self):
        response = self.app.get('/results/invalid_scan_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Scan not found', response.data)

    def test_processed_image_endpoint_invalid_scan_id(self):
        response = self.app.get('/processed_image/invalid_scan_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Image not found', response.data)

if __name__ == '__main__':
    unittest.main()