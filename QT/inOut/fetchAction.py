# encoding: utf-8
# author: LISICHENG
# software: PyCharm
# file: fetchAction.py
# time: 2020/5/15 11:20

import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Email:
    def __init__(self, sender='layhal@163.com', password='liu670', smtpserver='smtp.163.com'):
        self.sender = sender
        self.password = password
        self.smtpserver = smtpserver

    def send_email(self, receiver, msg, mail_title="提示信息"):
        mail_title = mail_title + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = MIMEText(msg, 'plain', 'utf-8')
        print(self.sender, receiver)
        message['From'] = self.sender  # 邮件上显示的发件人
        message['To'] = receiver  # 邮件上显示的收件人
        message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题
        smtp = smtplib.SMTP_SSL(self.smtpserver, 465)  # 创建一个连接
        # smtp.set_debuglevel(1)
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
        smtp.quit()