import io
import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from app.bot_init import password, my_email


def send_email(file: io.BytesIO, mail: str) -> bool:
    try:
        doc = file.getvalue()
        msg = msg_preparation(my_email, mail)
        file_path = file_path_preparation(doc)
        encoders.encode_base64(file_path)
        msg.attach(file_path)
        if job_with_server(my_email, password, mail, msg):
            return True
    except Exception as e:
        logging.exception(f'ошибка отправки на почту {e}')
        return False


def msg_preparation(sender: str, mail: str) -> MIMEMultipart:
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = mail
    msg['Subject'] = 'ИП Василевский'
    return msg


def file_path_preparation(doc) -> MIMEBase:
    file_path = MIMEBase('application', 'octet-stream', name='Файл_ворд.docx')
    file_path.set_payload(doc)
    file_path.add_header('Content-Disposition', 'attachment', filename='ИП Василевский.docx')
    return file_path


def job_with_server(sender, passw, mail, msg) -> bool:
    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
        server.login(sender, passw)
        server.sendmail(sender, mail, msg.as_string())
        server.quit()
        logging.info('Успешно отправил на почту')
        return True
