#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# google_email.py
#
# Copyright 2019 Aleksei Remnev <ran1024@yandex.ru>
#
import smtplib
import imaplib
import email.utils
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GoogleEmail:
    """
    Класс для работы с почтой через google mail.
    :param company: str() обычно ФИО отправителя или название компании отправителя.
    """
    def __init__(self, user_email='login@gmail.com', password='qwerty', company='MyCompany'):
        self.user_email = user_email
        self.password = password
        self.company = company
        self.gmail_smtp = 'smtp.gmail.com'
        self.gmail_imap = 'imap.gmail.com'

    def send_mail(self, addr_to, subject, msg_text, user_name='Recipient'):
        """
        Метод отправки почты.
        :param addr_to: str() - адресат
        :param subject: str() - тема письма
        :param msg_text: str() - тело письма
        :param user_name: str() обычно ФИО получателя письма
        :return: возвращает (0, str) если всё хорошо и (1, err) если ошибка соединения.
        """
        msg = MIMEMultipart('alternative')
        msg['To'] = email.utils.formataddr((user_name, addr_to))
        msg['From'] = email.utils.formataddr((self.company, self.user_email))
        msg['Subject'] = subject

        msg.attach(MIMEText(msg_text, 'plain'))
        msg.attach(MIMEText(f'<html><body><h4>{msg_text}</h4></body></html>', 'html'))
        msg.set_unixfrom('author')

        server = smtplib.SMTP(self.gmail_smtp, 587)
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.user_email, self.password)
            server.sendmail(self.user_email, addr_to, msg.as_string())
        except Exception as err:
            return 1, f'ERROR: {err}'
        finally:
            server.quit()
            return 0, 'Письмо отправлено.'

    def receive_mail(self, header=None):
        """
        Метод находит письмо по теме или получает последнее письмо из Inbox.
        :param header: str() - тема письма для поиска в Inbox.
        :return: возвращает (0, str(письмо)) или (1, err) в случае ошибки.
        """
        try:
            connection = imaplib.IMAP4_SSL(self.gmail_imap, 993)
            connection.login(self.user_email, self.password)
        except Exception as err:
            return 1, f'ERROR: {err}'

        rsp, data = connection.select('INBOX', readonly=True)
        if rsp == 'OK' and int(data[0].decode()) > 0:
            criterion = '(HEADER Subject "%s")' % header if header is not None else 'ALL'
            result, data = connection.uid('search', None, criterion)
            if not data[0]:
                return 1, 'По этому поиску ничего не найдено.'
            latest_email_uid = data[0].split()[-1]
            result, data = connection.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1].decode('utf8')
            email_message = email.message_from_string(raw_email)

            to_addr = make_header(decode_header(email_message["To"]))
            from_addr = make_header(decode_header(email_message["From"]))
            subject = make_header(decode_header(email_message["subject"]))
            mail_text = f'\nКому: {to_addr}\n'
            mail_text += f'От  : {from_addr}\n'
            mail_text += f'Тема: {subject}\n\n'
            maintype = email_message.get_content_maintype()
            if maintype == 'multipart':
                for part in email_message.get_payload():
                    if 'text/plain' in part['content-Type']:
                        mail_text += part.get_payload(decode=True).decode('utf8')
            elif maintype == 'text':
                mail_text += email_message.get_payload(decode=True).decode('utf8')

            connection.close()
            connection.logout()
        else:
            mail_text = 'Во входящих нет писем.'

        return 0, mail_text


def main():
    mail = GoogleEmail('ran1024440@gmail.com', 'Salmonella$@12')
    err, result = mail.send_mail('vasiapupkin@my_domen.ru', 'Пример',
                                  'Отправлено в целях тестирования.', 'Вася Пупкин')
    if err:
        print('Произошла ошибка при получении письма:')
    print(result)
    err, result = mail.receive_mail()
    if err:
        print('Произошла ошибка при получении письма:')
    print(result)


if __name__ == '__main__':
    import sys
    sys.exit(main())
