from rest_framework import serializers

from email_importer.models import EmailMessage


class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = ['subject', 'sent_date', 'body']