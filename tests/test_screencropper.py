from screencropper import crop
import unittest

class TestScreencropper(unittest.TestCase):
    def test_run(self):
        res = crop(save_screenshot=False)

        region, image = res
        
        self.assertEqual(len(res), 2)
        self.assertGreaterEqual(region[0], 0)
        self.assertGreaterEqual(region[1], 0)
        self.assertGreaterEqual(region[2], 0)
        self.assertGreaterEqual(region[3], 0)
        self.assertIsNotNone(image)
