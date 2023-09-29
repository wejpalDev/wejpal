from django.db import models
from authentications.models import User

# Create your models here.
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.email