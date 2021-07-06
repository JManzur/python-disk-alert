#!/usr/bin/env python3
import subprocess
import socket
import shutil
import time
import smtplib
from email.message import EmailMessage
import yaml
import logging

# Log level definition
logging.basicConfig(filename='disk_alert.log', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# Variables definition
now_date = (time.strftime("%Y-%m-%d - %H:%M"))
threshold = 90
partition = "/"

# Get Disk Usage
total, used, free = shutil.disk_usage(partition)
p_total = (total // (2**30))
p_used = (used // (2**30))
p_free = (free // (2**30))

# Get Hostname
hostname = socket.gethostname()
# Get IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = (s.getsockname()[0])
s.close()

# Mail credentials definition loaded from a yaml file
# If you use gmail, you must generate an "App Password" https://support.google.com/accounts/answer/185833?hl=en 
cred = yaml.safe_load(open('mail_cred.yml'))
EMAIL_ADDRESS = cred['ADDRESS']
EMAIL_PASSWORD = cred['PASSWORD']
RECIPIENTS = cred['SEND_TO']

# Send Mail funtion
def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'WARNING! Low disk space at ' + hostname
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENTS
    msg.set_content("""\
    Disk usage over than {0:} % of total capacity
    Date: {1:}

    Server hostname: {2:}
    IP: {3:}
    
    Partition: {4:}
    Total Size: {5:} GiB
    Total Used: {6:} GiB
    Total Free: {7:} GiB
    """.format(threshold, now_date, hostname, ip_address, partition, p_total, p_used, p_free))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

#Check disk funtion
def check_once():
    df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if splitline[5] == partition:
            if int(splitline[4][:-1]) > threshold:
                send_email()
                logging.warning("""NOT OK - Email alert has been sent - Partition: "{0:}", Size: {1:} GiB, Used: {2:} GiB, Free: {3:} GiB""".format(partition, p_total, p_used, p_free))
            if int(splitline[4][:-1]) < threshold:
                logging.info("""OK - Partition: "{0:}", Size: {1:} GiB, Used: {2:} GiB, Free: {3:} GiB""".format(partition, p_total, p_used, p_free))

if __name__ == "__main__":
    check_once()