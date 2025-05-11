from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.CharField(max_length=255)
    value = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def file_url(self):
        return self.file.url if self.file else ""

    def file_name(self):
        return self.file.name.split("/")[-1] if self.file else ""

    def file_size(self):
        return self.file.size if self.file else 0

    def __str__(self):
        return f'{self.user} - {self.value[:30]}'
        
