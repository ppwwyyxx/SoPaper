#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: mailutil.py
# Date: 五 6月 13 18:07:29 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from .textutil import title_beautify
from ukconfig import MAILSERVER_HOST, MAILSERVER_PORT

import json
import requests
import urllib.request, urllib.parse, urllib.error


PAT = "https://sopaper.net9.org/download?pid={0}"

def sendmail(addr, author, res):
    subject = "[SoPaper] Your Paper Request Has Been Processed"
    content = "Dear {0}, <br/>".format(addr)
    content += "Thanks for using <a href=\"https://sopaper.net9.org\">SoPaper</a>. You have recently requested for papers of {0}. ".format(title_beautify(author))
    content += "Here are the results:<br/><br/>"
    for idx, (pid, title) in enumerate(res):
        content += "<a href=\"{1}\">{2}. {0}</a><br/>\n".format(title_beautify(title), PAT.format(pid), idx)

    content += "<br/>Thanks for your support!<br/>"

    dic = {'addr': addr, 'subject': subject, 'content': content}
    headers = {'Content-type': 'application/json', 'Accept': '*/*'}
    resp = requests.post("http://{0}:{1}/mail".format(MAILSERVER_HOST, MAILSERVER_PORT),
                 data=json.dumps(dic), headers=headers)
    print(resp.content)


if __name__ == '__main__':
    sendmail('ppwwyyxxc@gmail.com', 'Yuxin Wu')
