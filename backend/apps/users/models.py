from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    chat_history = models.JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}, Username: {self.username}, Created At: {self.created_at}"
