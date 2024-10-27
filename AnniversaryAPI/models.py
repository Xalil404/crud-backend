from django.db import models
from django.contrib.auth.models import User

class Anniversary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Anniversary on {self.date}"

