from . config import setting
import smtplib
from fastapi import HTTPException, status
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template


def send_email(email, otp):
    from_email = setting.email
    password = setting.password
    to_email = email
    subject = "OTP for registration"
    
    #get current directory Path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    #get templates directory path
    templates_dir = os.path.join(current_dir,"..", "templates")
    
    #file name
    file_name = "email.html"

    #file path
    file_path = os.path.join(templates_dir, file_name)

    with open(file_path, "r") as f:
        template_str = f.read()

    template = Template(template_str)
    body = template.render(otp=otp)
    message = MIMEMultipart('alternative')
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))
    message.add_header('formate', 'flowed')
    message.add_header('Content-Disposition', 'inline')
    try:
        # Setup mail server and send email
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)  # Change this to your mail server
        mail_server.starttls()
        mail_server.login(from_email, password)
        mail_server.sendmail(from_email, to_email, message.as_string())
        mail_server.quit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="cannot send the email")