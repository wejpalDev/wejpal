from django.db import models
from authentications.models import User

# Create your models here.
class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    min_token_allowed = models.FloatField(default=0)
    token_credited = models.FloatField(default=0)
    token_paid_out = models.FloatField(default=0)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.title

class BetOption(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.name

class BetComment(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.name

class BetUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    bet_option = models.ForeignKey(BetOption, on_delete=models.CASCADE)
    token_on_bet = models.FloatField(default=0)
    token_paid_out = models.FloatField(default=0)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.token_on_bet
