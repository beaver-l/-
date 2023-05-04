# coding=utf-8
import smtplib
from email.mime.text import MIMEText

def stmp(msg_from='',passwd='',msg_to='',subject='',content=''):#依次为发送方邮箱，发送方授权码，接收人邮箱，邮件主题，邮件正文
    msg_from = msg_from  # 发送方邮箱
    passwd = passwd  # 填入发送方邮箱的授权码
    msg_to = msg_to  # 收件人邮箱

    subject = subject  # 主题
    content = content  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)# 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except:
        print('发送失败')