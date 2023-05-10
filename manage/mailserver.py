#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: mailserver.py
# Date: Sun Jun 29 10:05:10 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>


from flask import Flask, request
app = Flask(__name__)
import traceback

import smtplib
from email.mime.text import MIMEText

@app.route('/mail', methods=['POST'])
def mail():
    js = request.get_json(force=True)
    print(js)
    try:
        sendmail(js['addr'], js['subject'], js['content'])
    except Exception as e:
        traceback.format_exc()
        return {'status': 'error',
                'reason': str(e)}
    return {'status': 'ok'}

server = smtplib.SMTP('localhost')
def sendmail(addr, subject, content):
    me = 'sopaper@net9.org'
    you = addr
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    server.sendmail(me, [you], msg.as_string())

if __name__ == '__main__':
    app.run(port=5184, debug=True)

