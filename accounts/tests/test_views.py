import pytest 
from django.urls import reverse 
from accounts.models import CustomUser

@pytest.mark.django_db
class TestRegisterView:

    def test_register_page_loads(self, client):
        # Registration page must return 200
        response = client.get(reverse('register'))
        assert response.status_code == 200

    def test_register_creates_inactive_user(self, client):
        # User must be created as inactive until email is confirmed
        client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'Test1234!'
        })
        user = CustomUser.objects.get(username='newuser')
        assert user.is_active is False

    def test_register_duplicate_email_fails(self, client):
        # Duplicate email must not create a second user
        CustomUser.objects.create_user(
            username='existing',
            email='existing@test.com',
            password='Test1234!'
        )
        client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'existing@test.com',
            'password': 'Test1234!'
        })
        assert CustomUser.objects.filter(email='existing@test.com').count() == 1

@pytest.mark.django_db
class TestLoginView:

    def test_login_page_loads(self, client):
        # Login page must return 200
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_with_invalid_credentials(self, client):
        # Invalid credentials must redirect back to login
        response = client.post(reverse('login'), {
            'email': 'wrong@test.com',
            'password': 'wrongpassword'
        })
        assert response.status_code == 302
        assert '/login' in response['Location']

