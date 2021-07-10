import psutil
import socket
import time
import logging
import smtplib
from email.message import EmailMessage
import yaml

# Log level definition
logging.basicConfig(filename='wdisk_alert.log', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# threshold definition (percentage)
threshold = 50

# Get Date, Hostname and IP
now_date = (time.strftime("%Y-%m-%d - %H:%M"))
hostname = socket.gethostname()
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

def disk_var():
    for p in psutil.disk_partitions():
        if p.device == 'C:\\':
            devices = {}
            total_gb_long = psutil.disk_usage(p.mountpoint).total / 1024 / 1024 / 1024
            used_gb_long = psutil.disk_usage(p.mountpoint).used / 1024 / 1024 / 1024
            free_gb_long = psutil.disk_usage(p.mountpoint).free / 1024 / 1024 / 1024
            total_gb_short = "{:.2f}".format(total_gb_long)
            used_gb_short = "{:.2f}".format(used_gb_long)
            free_gb_short = "{:.2f}".format(free_gb_long)
            disk_used_percent = psutil.disk_usage(p.mountpoint).percent
            devices[p.device] = disk_used_percent
            file_system = p.fstype
            drive = p.device
            return drive, file_system, disk_used_percent, total_gb_short, used_gb_short, free_gb_short

def check_disk():
    for p in psutil.disk_partitions():
        if p.device == 'C:\\':
            devices = {}
            total_gb_long = psutil.disk_usage(p.mountpoint).total / 1024 / 1024 / 1024
            used_gb_long = psutil.disk_usage(p.mountpoint).used / 1024 / 1024 / 1024
            free_gb_long = psutil.disk_usage(p.mountpoint).free / 1024 / 1024 / 1024
            total_gb_short = "{:.2f}".format(total_gb_long)
            used_gb_short = "{:.2f}".format(used_gb_long)
            free_gb_short = "{:.2f}".format(free_gb_long)
            disk_used_percent = psutil.disk_usage(p.mountpoint).percent
            devices[p.device] = disk_used_percent
            file_system = p.fstype
            
            if disk_used_percent < threshold:
                send_email()
                logging.warning('Drive: "{0:}", Total Size: {1:} GiB, Used: {2:}, Free: {3:} GiB, Usage Percentage: {4:}%, File System: {5:}.'.format(p.device, total_gb_short, used_gb_short, free_gb_short, disk_used_percent, file_system))
                logging.warning('NOT OK - Email alert has been sent - Drive "{0:}" has a usage percentage greater than the defined threshold of {1:}%'.format(p.device, threshold))

            elif disk_used_percent > threshold:
                logging.info('Drive: "{0:}", Total Size: {1:} GiB, Used: {2:}, Free: {3:} GiB, Usage Percentage: {4:}%, File System: {5:}.'.format(p.device, total_gb_short, used_gb_short, free_gb_short, disk_used_percent, file_system))
                logging.info('OK - Drive "{0:}" has a usage percentage less than the defined threshold of {1:}%'.format(p.device, threshold))

# Send Mail funtion
def send_email():
    drive, file_system, disk_used_percent, total_gb_short, used_gb_short, free_gb_short=disk_var()
    msg = EmailMessage()
    msg['Subject'] = 'WARNING! Low disk space at ' + hostname
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENTS
    msg.set_content("""\
    Disk usage over than {0:} % of total capacity
    Date: {1:}

    Server hostname: {2:}
    IP: {3:}
    
    Drive: {4:}
    Total Size: {5:} GiB
    Total Used: {6:} GiB
    Total Free: {7:} GiB
    Used Percentage: {8:}%
    File System: {9:}
    """.format(threshold, now_date, hostname, ip_address, drive, total_gb_short, used_gb_short, free_gb_short, disk_used_percent, file_system))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    check_disk()