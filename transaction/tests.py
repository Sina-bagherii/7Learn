from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from .models import Transaction


TEST_DB = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


@override_settings(DATABASES=TEST_DB)
class TransactionReportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        Transaction.objects.create(
            user=self.user, transaction_type=Transaction.CHARGE, amount=2000
        )
        Transaction.objects.create(
            user=self.user, transaction_type=Transaction.PURCHASE, amount=800
        )

    def test_get_report_returns_queryset_with_annotations(self):
        report = Transaction.get_report()
        self.assertEqual(report.count(), 1)
        entry = report.get(pk=self.user.pk)
        self.assertEqual(entry.tr_count, 2)
        self.assertEqual(entry.balance, 1200)

    def test_get_total_balance_uses_report(self):
        data = Transaction.get_total_balance(user=None)
        self.assertEqual(data["total_balance"], 1200)
