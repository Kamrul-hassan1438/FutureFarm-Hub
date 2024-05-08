import smtplib
import random
import string

def generate_otp(length=6):
    """Generate a random OTP code."""
    otp = ''.join(random.choices(string.digits, k=length))
    return otp

def send_otp_email(email, otp):
    """Send OTP code to the user's email."""
    # SMTP server configuration (replace with your email server settings)
    smtp_server ='smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'futurefarmhub@gmail.com'
    smtp_password = 'bsbm spok ndwm ldqa'

    # Email content
    sender_email = 'futurefarmhub@gmail.com'
    receiver_email = email
    subject = 'Your OTP Code'
    body = f'Your OTP code is: {otp}'

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption
    server.login(smtp_username, smtp_password)  # Login to the email server

    # Create the email message
    message = f'Subject: {subject}\n\n{body}'

    # Send the email
    server.sendmail(sender_email, receiver_email, message)

    # Close the connection to the SMTP server
    server.quit()

# Example usage:
email = 'mhassan212153@bscse.uiu.ac.bd'
otp = generate_otp()
send_otp_email(email, otp)
print(f'OTP code sent to {email}')
