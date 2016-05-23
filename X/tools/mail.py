from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
 
from email.utils import COMMASPACE,formatdate
from email import encoders
from X.settings import email_server
 
import os
import re
 
#server['name'], server['user'], server['passwd']
def send_mail_func(server, fro, to, subject, text, files=[]):
    assert type(server) == dict 
    assert type(to) == list 
    assert type(files) == list 
 
    msg = MIMEMultipart() 
    msg['From'] = fro 
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', '
    msg['Bcc'] = fro
    msg['Date'] = formatdate(localtime=True) 
    msg.attach(MIMEText(text,_charset="gbk"))
 
    for file in files: 
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
        part.set_payload(open(file, 'rb'.read())) 
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
        msg.attach(part) 
 
    import smtplib 
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(fro, to, msg.as_string()) 
    smtp.close()

def send_mail(addr,subject, text):
    subject=subject.encode('gbk')
    send_mail_func(email_server,email_server['user'],addr,subject,text)
