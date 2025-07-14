import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email_via_sendgrid(to_email, subject, html_content):
    message = Mail( 
        from_email= settings.SENDGRID_FROM_EMAIL, 
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Sendgrid error: {e}")
        return None