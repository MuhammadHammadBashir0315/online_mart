import aiosmtplib
from email.message import EmailMessage

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "zia_online_mart@example.com"
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.example.com",
            port=587,
            username="your_username",
            password="your_password",
            use_tls=True,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False