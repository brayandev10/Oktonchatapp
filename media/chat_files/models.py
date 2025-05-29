from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
        
        
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # remplace CharField ici
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
        return f'{self.user.username} - {self.value[:30]}'

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    is_user1_typing = models.BooleanField(default=False)
    is_user2_typing = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat entre {self.user1.username} et {self.user2.username}"

class PrivateMessage(models.Model):
    chat = models.ForeignKey(PrivateChat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    file_description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.chat} : {self.content[:30]}"
        
        
from django.contrib.auth import get_user_model
from django.db import models
import uuid
from django.utils.text import slugify

User = get_user_model()

class Snippet(models.Model):
    LANGUAGE_CHOICES = [
        ("html", "HTML"),
        ("css", "CSS"),
        ("js", "JavaScript"),
        ("php", "PHP"),
        ("python", "Python"),
    ]
    DIFFICULTY = [
        ("easy", "Facile"),
        ("medium", "Moyen"),
        ("hard", "Avancé"),
    ]
    VISIBILITY = [("public", "Public"), ("private", "Privé")]

    title       = models.CharField(max_length=120)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    language    = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    difficulty  = models.CharField(max_length=10, choices=DIFFICULTY)
    tags        = models.CharField(max_length=250, blank=True,
                                   help_text="Liste de tags séparés par des virgules")
    visibility  = models.CharField(max_length=7, choices=VISIBILITY, default="public")
    license     = models.CharField(max_length=30, default="mit")
    # blocs de code
    html_code   = models.TextField(blank=True)
    css_code    = models.TextField(blank=True)
    js_code     = models.TextField(blank=True)
    # métadonnées
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="snippets")
    likes       = models.PositiveIntegerField(default=0)
    views       = models.PositiveIntegerField(default=0)
    is_draft    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
class SnippetLike(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet  = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name="liked_by")
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "snippet")
        
                                                        