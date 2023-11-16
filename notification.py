
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

import retrying

@retrying.retry(stop_max_attempt_number=3)
def send_mail(conf,content):
    mailfrom = conf['mailfrom']
    mailto=conf['mailto']
    passwd=conf['passwd']

    msg=MIMEMultipart()
    msg.attach(MIMEText(content['content'],'plain','utf-8'))
    msg['Subject']=Header(content['title'],'utf-8')
    msg['From']=mailfrom
    msg['To']=mailto

    sever='smtp.qq.com'
    smtp=SMTP_SSL(sever)
    smtp.set_debuglevel(0)
    smtp.ehlo(sever)
    smtp.login(mailfrom,passwd)
    smtp.sendmail(mailfrom,mailto,msg.as_string())
    smtp.quit()

    print('Mail sent.')
 


def notify(conf,msg):
    notify_conf=conf['notification']
    try:
        send_mail(notify_conf,msg)
    except Exception as e:
        print(e)
        print('Mail sent failed.')