from imaplib import IMAP4_SSL
import email
from email.utils import parsedate_to_datetime
from email.policy import default
from bs4 import BeautifulSoup

USER: str = 'mishah238@gmail.com'
PASSWORD: str = 'sxbf hxgq syad gwvj'
HOST: str = 'imap.gmail.com'


with IMAP4_SSL(HOST) as M:
    M.login(USER, PASSWORD)
    M.select()
    typ, data = M.search(None, 'ALL')

    all_messages = data[0].split()
    last_10_messages = all_messages[-10:]  # Получаем последние 10 сообщений

    for num in last_10_messages:
        typ, data = M.fetch(num, '(RFC822)')
        raw_email = data[0][1]

        # Преобразуем сырое сообщение в объект email.message.EmailMessage
        msg = email.message_from_bytes(raw_email, policy=default)

        # Извлекаем тему сообщения
        subject = msg["subject"]

        # Извлекаем дату отправки
        sent_date = msg["date"]
        sent_date = parsedate_to_datetime(sent_date) if sent_date else "Дата не указана"

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
        clean_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())


def topic(user, password, host):
    with IMAP4_SSL(HOST) as M:
        M.login(USER, PASSWORD)
        M.select()
        typ, data = M.search(None, 'ALL')

        all_messages = data[0].split()
        last_10_messages = all_messages[-10:]  # Получаем последние 10 сообщений

        for num in last_10_messages:
            typ, data = M.fetch(num, '(RFC822)')
            raw_email = data[0][1]

            # Преобразуем сырое сообщение в объект email.message.EmailMessage
            msg = email.message_from_bytes(raw_email, policy=default)

            # Извлекаем тему сообщения
            subject = msg["subject"]

            # Извлекаем дату отправки
            sent_date = msg["date"]
            sent_date = parsedate_to_datetime(sent_date) if sent_date else "Дата не указана"

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
            clean_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())

            # Выводим нужные данные
            print(f"Тема: {subject}")
            print("=" * 50)  # Разделитель для наглядности

