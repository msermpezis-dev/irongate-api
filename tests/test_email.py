from unittest import TestCase

from application.email_plus.email import Email


class EmailTestCase(TestCase):
    def test_email_success(self):
        is_email = Email().check_email("test@test.com")
        self.assertTrue(is_email)

    def test_email_failure(self):
        is_email = Email().check_email("test.com")
        self.assertFalse(is_email)