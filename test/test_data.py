import os
import unittest

from pollingclient.client import PollingClient


class TestData(unittest.TestCase):

    def setUp(self):
        self._client = PollingClient(os.path.join(os.path.dirname(__file__), "data"))

    def test_parties(self):
        df = self._client.parties
        self.assertEquals(df.shape[0], 6041)

    def test_leaders(self):
        df = self._client.leaders
        self.assertEquals(df.shape[0], 1861)

    def test_in_power(self):
        df = self._client.in_power
        self.assertEquals(df.shape[0], 19)

    def test_general_elections(self):
        df = self._client.in_power
        self.assertEquals(df.shape[0], 19)
