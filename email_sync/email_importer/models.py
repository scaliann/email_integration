from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class EmailAccount(models.Model):
    SERVICE_CHOICES = [
        ('yandex', 'Yandex'),
        ('gmail', 'Gmail'),
        ('mailru', 'Mail.ru'),
    ]

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    imap_host = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.get_service_display()} - {self.email}"


class EmailMessage(models.Model):
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name="messages")
    uid = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()

    def __str__(self):
        return f"{self.subject} ({self.sent_date.strftime('%Y-%m-%d')})"


class EmailAttachment(models.Model):
    email_message = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='attachments/')
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Attachment: {self.file_name} for {self.email_message.subject}"