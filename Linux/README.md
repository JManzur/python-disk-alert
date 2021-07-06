
# Check linux disk capacity and send an email alert

This simple Python script scans a given linux disk (mount point path) and, based on a specified percentage threshold, triggers an email notification that includes a detailed summary of the server and current disk usage. Also a log file is generated every time that the script is run

## Tested with: 

| Environment | Application | Version  |
| ----------------- |-----------|---------|
| WSL2 Ubuntu 20.04 | Python | 3.8.5 |
| Ubuntu 18.04 | Python | 3.6.9 |

## How-To

First you need to create a file called "mail_cred.yml" located in the root folder with a content similar to the following:

```bash
ADDRESS: 'sender@gmail.com'
PASSWORD: 'xxxxxxxxxxxxxxxxx'
SEND_TO: 'recipient@example.com'
#SEND_TO: 'one@example.com, two@example.com, three@example.com'
```
After that you need to install the necessaries python requirements, by runing:

```bash
pip3 install -r requirements.txt
```
Finally, set the variables "threshold" and "partition" to whatever you decide and by doing that, you are all set. Now you can test the script:

```bash
python3 linux_disk_alert.py
```
And when you're ready go ahead and set up a cron job to run it on a regular basis. In my case (because I'm using the PyYAML module to load the email credential), I'm calling a simple bash script from crontab:

Script:
```bash
#!/bin/bash
cd /opt/scripts/disk_alert
python3 linux_disk_alert.py
```

Cron job:
```bash
# Python Disk-Alert [Run daily at 23:30]:
30 23 * * * /opt/scripts/disk_alert/run_script.sh
```

**NOTE**: Change the paths as required

## Log file

Every time you run the script, a file called "disk_alert.log" will be generated/updated with information similar to the following:

```log
2021-07-06 12:55:23,354: WARNING: NOT OK - Email alert has been sent - Partition: "/", Size: 250 GiB, Used: 2 GiB, Free: 235 GiB
2021-07-06 12:56:03,972: INFO: OK - Partition: "/", Size: 250 GiB, Used: 2 GiB, Free: 235 GiB
```

**Note**: To capture this sample output, I change the "threshold" value, that's why the disk usage is the same in both cases.

## Author

- [@JManzur](https://www.github.com/jmanzur)

## Documentation

- [Logging Module](https://docs.python.org/3/library/logging.html#module-logging)
- [PyYAML Module](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Google App Passwords](https://support.google.com/accounts/answer/185833?hl=en)