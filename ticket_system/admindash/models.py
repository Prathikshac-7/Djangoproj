from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Agent', 'Agent'),
        ('Customer', 'Customer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    # Tickets can be assigned to multiple agents; blank=True makes it optional.
    agents = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title
