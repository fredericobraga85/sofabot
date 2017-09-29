from django.test import TestCase

from SofaBot.SofaBotApp.utils.Bitfinex import BitFinex
from django.conf import settings

class BitFinexTests(TestCase):
    def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
        settings.configure()

    def testBalances(self):

        bitfinex = BitFinex()
        bitfinex.getBalances()