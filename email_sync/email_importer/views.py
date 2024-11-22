from datetime import timezone
from email.policy import default
from imaplib import IMAP4_SSL

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet
from imapclient import IMAPClient
import email
from email.utils import parsedate_to_datetime
from .models import EmailMessage, EmailAccount
from email_importer.models import EmailMessage
from email_importer.serializers import EmailMessageSerializer
from django.utils import timezone

USER: str = 'mishah238@gmail.com'
PASSWORD: str = 'sxbf hxgq syad gwvj'
HOST: str = 'imap.gmail.com'
def message_list(request):
    return render(request, 'index.html')

def fetch_and_save_messages(email_account):
    """Подключается к почтовому ящику, получает последние 10 сообщений и сохраняет их в базе данных."""
    with IMAP4_SSL(email_account.imap_host) as M:
        M.login(email_account.email, email_account.password)
        M.select()

        # Получаем последние 10 сообщений по UID
        typ, data = M.search(None, 'ALL')
        all_messages = data[0].split()
        last_10_uids = all_messages[-1000:]  # Получаем последние 10 сообщений по UID

        for uid in last_10_uids:
            # Проверяем, существует ли уже сообщение с этим UID
            if EmailMessage.objects.filter(uid=uid, email_account=email_account).exists():
                continue  # Пропускаем, если уже существует

            typ, data = M.fetch(uid, '(RFC822)')
            raw_email = data[0][1]

            # Преобразуем сырое сообщение в объект email.message.EmailMessage
            msg = email.message_from_bytes(raw_email, policy=default)

            # Извлекаем тему сообщения
            subject = msg["subject"]

            # Извлекаем дату отправки
            sent_date = msg["date"]
            sent_date = parsedate_to_datetime(sent_date) if sent_date else timezone.now()

            # Извлекаем текстовую часть или очищаем HTML
            content = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True).decode()
                    break
                elif part.get_content_type() == "text/html" and not content:
                    soup = BeautifulSoup(part.get_payload(decode=True).decode(), "html.parser")
                    content = soup.get_text()

            # Удаляем лишние пустые строки и пробелы
            body = "\n".join(line.strip() for line in content.splitlines() if line.strip())

            # Сохраняем сообщение в базе данных
            EmailMessage.objects.create(
                email_account=email_account,
                uid=uid,
                subject=subject,
                sent_date=sent_date,
                received_date=timezone.now(),
                body=body
            )


def update_messages(request):
    # Получаем аккаунт, который будем обновлять
    # Здесь, для примера, мы просто берем первый аккаунт из базы данных
    email_account = EmailAccount.objects.first()

    if email_account:
        fetch_and_save_messages(email_account)
        return JsonResponse({"status": "Messages updated successfully"})
    else:
        return JsonResponse({"status": "No email account found"}, status=404)




from email_sync.test import topic


class EmailMessageView(ModelViewSet):

    queryset = EmailMessage.objects.all()[:50]
    serializer_class = EmailMessageSerializer

