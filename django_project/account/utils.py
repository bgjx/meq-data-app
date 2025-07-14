import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email_via_sendgrid(to_email, subject, html_content):
    """
    Sends an email using SendGrid.

    This function constructs an email message with the provided recipient,
    subject, and HTML content, and sends it via the SendGrid API. If the
    email is sent successfully, it returns the HTTP status code of the 
    SendGrid API response. If an error occurs, it catches the exception,
    prints an error message, and returns None.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        html_content (str): The HTML content of the email.

    Returns:
        Optional[int]: The HTTP status code from SendGrid's response,
                       or None if an error occurred.
    """
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