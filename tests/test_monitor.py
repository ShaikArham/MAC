import unittest
from pipelines.export_preview import build
class MonitorTest(unittest.TestCase):
    def test_monitoring(self):
        s=build(); m=s['monitoring']
        self.assertEqual(len(m['sources']),10)
        self.assertEqual(sum(x['rows'] for x in m['sources']),22)
        self.assertEqual(m['counts'],dict(bronze=22,silver=17,quarantine=5))
        self.assertEqual(len(m['rejections']),5)
        self.assertEqual(m['batches'][0]['status'],'success')
        self.assertEqual(m['audit'][0]['event'],'batch_success')
