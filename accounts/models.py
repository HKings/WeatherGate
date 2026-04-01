from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

class CustomUser(AbstractUser):
    # MFA token sent by rmail (6 digits)
    mfa_token = models.CharField(max_length=6, blank=True, null=True)
    
    # Token expiration timestamp
    mfa_token_created_at = models.DateTimeField(blank=True, null=True)

    # Whether MFA has been verified in current session
    mfa_verified = models.BooleanField(default=False)

    def generate_mfa_token(self):
        # Generates a random 6-digit numeric token
        self.mfa_token = ''.join(random.choice(string.digits, k=6))
        return self.mfa_token
    
    def __str__(self):
        return self.email

