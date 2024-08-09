from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Problem for {self.user.username}"
