import smtplib
import ssl

sender_email = "testezzone1@gmail.com"
receiver_email = "ceofourfactplus@gmail.com"
password = 'test14/12/2021'
# Subject: Hi there
message = 'test'

# This message is sent from Python."""

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
