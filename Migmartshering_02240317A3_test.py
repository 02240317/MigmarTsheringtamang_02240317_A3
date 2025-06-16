import unittest
from Migmartshering_02240317_A3 import (SecureBankAccount, DigitalBank)

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        """Initialize test environment"""
        self.bank = DigitalBank()
        self.test_acc = SecureBankAccount("TEST001", "1234", "Personal")
        self.test_acc.funds = 1000.0
        self.recipient = SecureBankAccount("TEST002", "5678", "Business")
        self.recipient.funds = 500.0
        self.bank.accounts = {
            "TEST001": self.test_acc,
            "TEST002": self.recipient
        }

    # Test unusual inputs
    def test_invalid_amounts(self):
        """Test handling of invalid transaction amounts"""
        with self.assertRaises(ValueError):
            self.test_acc.add_funds(-100)  # Negative deposit
        with self.assertRaises(ValueError):
            self.test_acc.remove_funds(0)  # Zero withdrawal
        with self.assertRaises(ValueError):
            self.test_acc.add_phone_credit(1000000, "1234567890")  # Excessive amount

    # Test invalid function usage
    def test_invalid_operations(self):
        """Test error handling for invalid operations"""
        with self.assertRaises(ValueError):
            self.test_acc.remove_funds(2000)  # Overdraft attempt
        with self.assertRaises(ValueError):
            self.test_acc.add_phone_credit(100, "123")  # Invalid phone
        with self.assertRaises(ValueError):
            self.test_acc.send_money(500, None)  # None recipient

    # Test core banking methods
    def test_deposit_operation(self):
        """Test successful deposit"""
        self.test_acc.add_funds(500)
        self.assertEqual(self.test_acc.funds, 1500.0)
        self.assertIn("Deposit: +$500.00", self.test_acc.transaction_history)

    def test_withdraw_operation(self):
        """Test successful withdrawal"""
        self.test_acc.remove_funds(200)
        self.assertEqual(self.test_acc.funds, 800.0)
        self.assertIn("Withdrawal: -$200.00", self.test_acc.transaction_history)

    def test_transfer_operation(self):
        """Test money transfer between accounts"""
        self.test_acc.send_money(300, self.recipient)
        self.assertEqual(self.test_acc.funds, 700.0)
        self.assertEqual(self.recipient.funds, 800.0)

    def test_phone_topup(self):
        """Test mobile credit purchase"""
        self.test_acc.add_phone_credit(50, "1234567890")
        self.assertEqual(self.test_acc.phone_credit, 50.0)
        self.assertEqual(self.test_acc.funds, 950.0)

    def test_account_closure(self):
        """Test account deletion"""
        self.assertTrue(self.bank.close_account("TEST001"))
        self.assertNotIn("TEST001", self.bank.accounts)

if __name__ == "__main__":
    unittest.main()