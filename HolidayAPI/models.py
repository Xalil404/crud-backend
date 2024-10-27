from django.db import models
from django.contrib.auth.models import User

class Holiday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()  # Month as an integer (1-12)
    day = models.IntegerField()     # Day as an integer (1-31)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
