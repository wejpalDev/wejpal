from django.db import models
from authentications.models import User

# Create your models here.
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(null=True, default=0)
    paused_balance = models.FloatField(null=True, default=0)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.balance

class TokenHistory(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    balance_before = models.FloatField(null=True, default=0)
    balance_after = models.FloatField(null=True, default=0)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.balance_before