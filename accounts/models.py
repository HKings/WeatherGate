from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import random
import string

class CustomUser(AbstractUser):
    
    mfa_token = models.CharField(max_length=6, blank=True, null=True) # MFA token sent by email (6 digits)
    mfa_token_created_at = models.DateTimeField(blank=True, null=True) # Token expiration timestamp
    mfa_verified = models.BooleanField(default=False) # Whether MFA has been verified in current session
    is_email_verified = models.BooleanField(default=False) # Whether email has been confirmed after registration

    def generate_mfa_token(self):
        # Generates a random 6-digit numeric token and saves the creation time
        self.mfa_token = ''.join(random.choices(string.digits, k=6))
        self.mfa_token_created_at = timezone.now()
        return self.mfa_token
    
    def is_mfa_token_valid(self):
        # Returns True if the token was generated less than 10 minutes ago
        if not self.mfa_token_created_at:
            return False
        expiration_time = self.mfa_token_created_at + timedelta(minutes=10)
        return timezone.now() < expiration_time


    def __str__(self):
        return self.email

