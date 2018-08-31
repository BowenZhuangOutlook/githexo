#!/usr/bin/python
# -*- coding:utf-8 -*-  
import datetime
import os, sys
import subprocess
import socket
HOSTNAME = socket.gethostname()

base_config = {
    "dbhost": "mongodb://%s/?ssl=true&ssl_ca_certs=/etc/ssl/ca.cer" % HOSTNAME,
    "dbport": 27017,
    "dbuser": "xxxxxxxxx",
    # password need encrypted via base64.encodestring(plaintext)
    "dbpass": "xxxxxxxxx"
}

mg_slow_query_config = {
    #configure slow query save folder and process execute log location.
    "output": "/home/mongod/report/slow",
	#configure mongodb slow query time range
    "gttime": datetime.datetime.combine(datetime.date.today(), datetime.time.min) - datetime.timedelta(days=1),
    "lttime": datetime.datetime.now(),
	#configure mongod slow filter condition
    "slowms": 1000,
    "slowcnt": 1,
	#filter collection. e.g fqdb.fastquote
    "slowcollection": [],
	#fliter db name
    "slowdbname": ["admin", "local"],
	#configure email header,CC,TO
    "Eheader": "Get Mongodb Slow Log",
    "ECC": " ",
    "ETO": "xxxxxxxxx"
}

'''
Below common functions 
'''

CMD_EMAIL = '''
mailx -s "{0}" "{1}" "{2}" < {3}
'''


def send_mail(header, cc, to, logfile):
    print(CMD_EMAIL.format(header, cc, to, logfile))
    p = subprocess.Popen(CMD_EMAIL.format(header, cc, to, logfile), shell=True, stdout=subprocess.PIPE)
    output, errors = p.communicate()
    return errors, output


class Logger(object):
    def __init__(self, filename):
        filedir = os.path.dirname(filename)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass
