from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os
import smtplib 
from email.mime.multipart import MIMEMultipart
import csv
from dotenv import load_dotenv
from email.header import Header
load_dotenv();


def add_coverletter(msg, recruiter_name, company_name):
    coverletter_text = COVERLETTER_TEXT.format(recruiter_field = recruiter_name, company_field = company_name)
    msg.attach(MIMEText(coverletter_text))
  
        
def connect_to_server(email, password):
    print("[?] Connecting to server...")  
    mail_port= 587
    my_server = smtplib.SMTP(SMTP_SERVER, mail_port)
    my_server.ehlo()
    my_server.starttls()
    my_server.login(email, password)
    print("[+] Connection established.")
    return my_server


def add_attachment(msg, filename, filepath = ""):
    if filepath == "": filepath = filename
    with open(filepath, 'rb') as f:
        file = MIMEApplication(
            f.read(),
            name=filename
        )
        file['Content-Disposition'] = f'filename="{filename}"'
        msg.attach(file)

def send_messages(csv_filename):
    csv_file = open(csv_filename)
    lines = csv.reader(csv_file)
    next(lines) #skips first line (Recruiter Name,Company Name,E-mail Address)
        
    for recruiter_name, company_name, receiver_mail in lines:
        recruiter_name = recruiter_name.title()
        company_name = company_name.title()
        receiver_mail = receiver_mail.lower()
        
        print(f"[?] An e-mail will be send to {company_name} company at {receiver_mail}")
        
        # create mime object
        message = MIMEMultipart("alternative")

        # set topic
        message['Subject'] = SUBJECT
        sender_name = Header(SENDER_NAME, 'utf-8').encode()
        message['From'] = f'{sender_name} <{EMAIL_ADDRESS}>'
        message['To'] = receiver_mail
        
        # checks if recruiter_name exists 
        if recruiter_name=="":recruiter_name = company_name + " Hiring Manager"
        
        # add text content
        add_coverletter(message, recruiter_name, company_name)

        # add resume and transkript
        add_attachment(message, RESUME_PATH)
        add_attachment(message, TRANSKRIPT_PATH)
        server.send_message(message)
        
        print(f"[+] An e-mail has been sent to {company_name} company at {receiver_mail}")
    
    csv_file.close()

    
if __name__ == "__main__":
    # creditentials
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    PASSWORD_KEY = os.environ.get("PASSWORD_KEY")
    CSV_FILENAME = "data.csv"
    
    # If you are using Gmail, comment out Outlook.
    SMTP_SERVER = "smtp-mail.outlook.com"
    # SMTP_SERVER = "smtp.gmail.com"
    
    # MAIL DETAILS
    SUBJECT = 'Internship Application'
    SENDER_NAME = "Your Name"
    RESUME_PATH = "resume-latest.pdf"
    TRANSKRIPT_PATH = "transkript.pdf"
    
    # recruiter_field and company_field will be replaced by data in data.csv
    COVERLETTER_TEXT = """
Dear {recruiter_field},

I am writing to express my interest in data science position at {company_field}. With a strong foundation in computer science and a passion for innovation, I am eager to contribute to your team and gain valuable hands-on experience.

Thank you for considering my application.

Sincerely,
[Your Name]
"""

    server = connect_to_server(EMAIL_ADDRESS, PASSWORD_KEY)
    send_messages(CSV_FILENAME)
    server.quit()