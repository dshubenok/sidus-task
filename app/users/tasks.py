from app import settings
from app.routines.app import celery_app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template


@celery_app.task(name="greetings_email", acks_late=True)
def greetings_email(email: str, first_name: str, last_name: str):
    message = MIMEMultipart('alternative')

    payload = {"first_name": first_name, "last_name": last_name}

    template = Template("Hello, {{first_name}} {{last_name}}!")
    content = template.render(**payload)

    message["Subject"] = "Wellcome to our platform!"
    message["From"] = settings.email_account
    message["To"] = email

    message.attach(MIMEText(content, 'plain'))
    message.attach(MIMEText(content, 'html'))

    connection = smtplib.SMTP(
        host=settings.email_server,
        port=settings.email_port
    )

    connection.ehlo()
    connection.starttls()
    connection.ehlo()

    connection.login(settings.email_account, settings.email_password)
    connection.sendmail(settings.email_account, email, message.as_string())

    connection.close()

    return {
        "sent_to": email,
        "payload": payload
    }
