import pytest
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser


@pytest.mark.django_db
class TestCustomUser:

    def test_generate_mfa_token_has_six_digits(self):
        # Token must be exactly 6 digits
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='Test1234!'
        )
        token = user.generate_mfa_token()
        assert len(token) == 6
        assert token.isdigit()

    def test_mfa_token_is_valid_within_10_minutes(self):
        # Token generated now must be valid
        user = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@test.com',
            password='Test1234!'
        )
        user.generate_mfa_token()
        user.save()
        assert user.is_mfa_token_valid() is True

    def test_mfa_token_is_expired_after_10_minutes(self):
        # Token generated 11 minutes ago must be invalid
        user = CustomUser.objects.create_user(
            username='testuser3',
            email='test3@test.com',
            password='Test1234!'
        )
        user.generate_mfa_token()
        user.mfa_token_created_at = timezone.now() - timedelta(minutes=11)
        user.save()
        assert user.is_mfa_token_valid() is False