import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(recipient_email,subject,message):
    sender_email = "futurefarmhub@gmail.com"
    sender_password = "bsbm spok ndwm ldqa"
    try:

        # Set up the SMTP server
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(sender_email, sender_password)

        # Create a message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send the message
        smtp_server.send_message(msg)

        # Close the connection
        smtp_server.quit()

        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



