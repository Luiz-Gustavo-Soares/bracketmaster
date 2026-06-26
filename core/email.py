from django.core.mail.backends.base import BaseEmailBackend
import requests
from bracketmaster import settings


class BrevoEmailBackend(BaseEmailBackend):
    API_URL = "https://api.brevo.com/v3/smtp/email"

    def send_messages(self, email_messages):
        enviados = 0

        for message in email_messages:

            payload = {
                "sender": {
                    "email": settings.DEFAULT_FROM_EMAIL,
                },
                "to": [
                    {"email": email}
                    for email in message.to
                ],
                "subject": message.subject,
            }

            # Texto simples
            if message.body:
                payload["textContent"] = message.body

            # HTML
            if hasattr(message, "alternatives"):
                for content, mimetype in message.alternatives:
                    if mimetype == "text/html":
                        payload["htmlContent"] = content
                        break

            # CC
            if message.cc:
                payload["cc"] = [
                    {"email": email}
                    for email in message.cc
                ]

            # BCC
            if message.bcc:
                payload["bcc"] = [
                    {"email": email}
                    for email in message.bcc
                ]

            # Reply-To
            if message.reply_to:
                payload["replyTo"] = {
                    "email": message.reply_to[0]
                }

            # Anexos
            if message.attachments:
                payload["attachment"] = []

                for attachment in message.attachments:

                    if len(attachment) != 3:
                        continue

                    filename, content, mime = attachment

                    import base64

                    payload["attachment"].append({
                        "name": filename,
                        "content": base64.b64encode(content).decode()
                    })

            response = requests.post(
                self.API_URL,
                headers={
                    "accept": "application/json",
                    "api-key": settings.BREVO_API_KEY,
                    "content-type": "application/json",
                },
                json=payload,
                timeout=15,
            )

            if response.ok:
                enviados += 1
            elif not self.fail_silently:
                response.raise_for_status()

        return enviados
