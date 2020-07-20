import unittest
from django.contrib.auth.models import User
from pays.models import FillUpTransaction, Wallet


class FillUpTestCase(unittest.TestCase):
    FILLUP_SUM = 10
    OLD_ACC = None
    NEW_ACC = None

    def setUp(self):
        usr = User.objects.get_or_create(
            username='test',
            password='H^ihds#2975',
            email='test@ya.ru'
        )
        wal = Wallet.objects.get(user=usr[0])
        self.OLD_ACC = wal.amount
        FillUpTransaction.objects.create(
            to_wallet=wal,
            amount=self.FILLUP_SUM
        )
        self.NEW_ACC = wal.amount

    def tearDown(self):
        pass

    def test_transact(self):
        self.assertEqual(self.OLD_ACC+self.FILLUP_SUM, self.NEW_ACC)


if __name__ == '__main__':
    unittest.main()
