import email
import imaplib
import smtplib
import time
from bardapi import Bard
from email import message_from_string

user = 'youremail@gmail.com'
password = 'Yourpassword'
token = 'you bard token'

def check(q, to, token, user, password):
    bard = Bard(token=token)
    print(q)
    resp = bard.get_answer(q)['content']
    print(resp)
    send(resp, to, user, password)

def send(body, to, user, password):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user,password)

    subject = 'Yeshvish Bard'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(user,to,msg)
    print('sent')
    server.quit()

def main(user,password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user,password)
    mail.list()
    mail.select("bard")
    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)") 

    msg = email.message_from_string(data[0][1].decode('utf-8'))
    
    return msg

global code1
code1 = main(user, password)['Message-ID']

while(True):
    msg = main(user,password)
    ID = msg['Message-ID']
    if ID != code1:
        try:
            msg1 = msg['subject']
            print(msg1)
            to = msg['Return-Path']
            to = str(to)
            to = to.strip('<')
            to = to.strip('>')
            check(msg1, to, token)
            code1 = ID
        except:
            print("err")
        time.sleep(5)
