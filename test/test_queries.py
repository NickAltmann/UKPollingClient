import os
import unittest
import datetime

from pollingclient.client import PollingClient


class TestQueries(unittest.TestCase):

    def setUp(self):
        self._client = PollingClient(os.path.join(os.path.dirname(__file__), "data"))

    def test_list_parties(self):
        ll = self._client.list_parties()
        self.assertEquals(len(ll), 5)

    def test_list_pollsters(self):
        pollsters = self._client.list_pollsters()
        self.assertIn("yougov", pollsters)

    def test_list_leaders(self):
        leaders = self._client.list_leaders()
        self.assertIn("Farron", leaders)

    def test_party_in_power(self):
        self.assertTrue(self._client.party_in_power("Con", datetime.datetime(2014, 1, 1)))
        self.assertTrue(self._client.party_in_power("LD", datetime.datetime(2014, 1, 1)))
        self.assertFalse(self._client.party_in_power("Lab", datetime.datetime(2014, 1, 1)))
        self.assertTrue(self._client.party_in_power("Lab", datetime.datetime(2004, 1, 1)))

    def test_get_leader_ratings(self):
        df = self._client.get_leader_ratings("Duncan Smith")
        self.assertEquals(df.shape[0], 24)

    def test_monthly_average(self):
        df = self._client.monthly_average()
        self.assertAlmostEqual(df.loc[datetime.datetime(2016, 12, 1), "Con"], 40.)

    def test_compare_ratings(self):
        df = self._client.compare_ratings(["Miliband", "Corbyn"], "Sat")
        self.assertEquals(df.shape, (20, 2))