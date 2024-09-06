# Get the Gmail credentials and build service
from abstra.connectors import get_gmail_credentials
from googleapiclient.discovery import build

# Build email message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Encode the message
from email import encoders
import base64


# Load the Google Cloud credentials and create the service
credentials = get_gmail_credentials()
service = build('gmail', 'v1', credentials=credentials)

# Email parameters and content
sender = 'sample@sample.com'
to = 'sample@sample.com'
subject = "Gmail Automation With Python"
message_text = "Here is some info about our services: We provide custom software development, IT consulting, and tailored support."

html_card = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Email</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #fffff; margin: 0; padding: 0;">
    <div style="max-width: 960px; margin: 0 auto; padding: 50px 0 50px 0;">
        <div style="background-color: #ffe0ef; width: 300px; margin: 0 auto; padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="font-size: 24px; color: #333;">Welcome to Our Service</h1>
            <p style="font-size: 16px; color: #666;">Your journey starts here!</p>
        </div>
    </div>
</body>
</html>
"""

file_path = 'attachment.pdf'

# Create the email message with multiple parts
message = MIMEMultipart()
message['to'] = to
message['from'] = sender
message['subject'] = subject


# Attach the message text
message.attach(MIMEText(message_text, 'plain'))


# Attach the message and the HTML card
message.attach(MIMEText(html_card, 'html'))


# Attach the file
with open(file_path, 'rb') as attachment:
    mime_base = MIMEBase('application', 'octet-stream')
    mime_base.set_payload(attachment.read())
    encoders.encode_base64(mime_base)
    mime_base.add_header('Content-Disposition', f'attachment; filename={file_path}')
    message.attach(mime_base)


# Encode the message and send it
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
print(f'Message Id: {message["id"]}')
