import os

import unittest
from leases import app

here = os.path.abspath(os.path.basename(__file__))

class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_correctLeasesAreShown(self):
        rv = self.client.get('/')
        assert bytes('OK_Host', 'utf-8') in rv.data
        assert bytes('Microsoft_Host', 'utf-8') in rv.data

    def test_outdatedLeasesAreNotShown(self):
        rv = self.client.get('/')
        assert bytes('Old_Lease_Host', 'utf-8') not in rv.data

if __name__ == '__main__':
    unittest.main()