from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date
from django.utils import timezone

current_datetime = timezone.now()
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.content}'
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="photos/")

    def __str__(self):
        return f'{self.id}'
class ExtraService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'
class Reservation(models.Model):
    username = models.ForeignKey(User,related_name='Booked_by', on_delete=models.CASCADE)
    room = models.ForeignKey(Room,related_name='Room_booked', on_delete=models.CASCADE)
    start_date = models.DateTimeField(validators=[MinValueValidator(limit_value=current_datetime)])
    end_date = models.DateTimeField(validators=[MinValueValidator(limit_value=current_datetime)])  
    extra_services = models.ManyToManyField(ExtraService, blank=True)
    
    def __str__(self):
        return f'{self.username} -> {self.room}'

 