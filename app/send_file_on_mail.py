import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from app.bot_init import password


def send_email(file, mail: str):
    sender = "gruzikom@mail.ru"
    passw = password
    try:
        doc = file.getvalue()
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = mail
        msg['Subject'] = 'ИП Василевский'
        file_path = MIMEBase('application', 'octet-stream', name='Файл_ворд.docx')
        file_path.set_payload(doc)
        file_path.add_header('Content-Disposition', 'attachment', filename='ИП Василевский.docx')
        encoders.encode_base64(file_path)
        msg.attach(file_path)
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(sender, passw)
        server.sendmail(sender, mail, msg.as_string())
        server.quit()
        logging.info('Успешно отправил на почту')
        return True
    except:
        logging.exception('ошибка отправки на почту')
        return False