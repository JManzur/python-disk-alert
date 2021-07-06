
# Check linux disk capacity and send an email alert

This simple Python script scans a given linux disk (mount point path) and, based on a specified percentage threshold, triggers an email notification that includes a detailed summary of the server and current disk usage. Also a log file is generated every time that the script is run

## Tested with: 

| Environment | Application | Version  |
| ----------------- |-----------|---------|
| WSL2 Ubuntu 20.04 | Python | 3.8.5 |
| Ubuntu 18.04 | Python | 3.6.9 |

## How-To

First you need to create a file called "mail_cred.yml" located in the root folder with content similar to the following:

```bash
ADDRESS: 'sender@gmail.com'
PASSWORD: 'xxxxxxxxxxxxxxxxx'
SEND_TO: 'recipient@example.com'
#SEND_TO: 'one@example.com, two@example.com, three@example.com'
```
After that you need to install the necesaries python requirements runing:

```bash
pip3 install -r requirements.txt
```
Finally, set the variables "threshold" and "partition" to whatever you decide and by doing that, you are all set. Now you can test the script:

```bash
python3 linux_disk_alert.py
```
And when you're ready, go ahead and set up a cron job to run it on a regular base

## Logging Levels

- **DEBUG**: Detailed information, typically of interest only when diagnosing problems.
- **INFO**: Confirmation that things are working as expected.
- **WARNING**: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
- **ERROR**: Due to a more serious problem, the software has not been able to perform some function.
- **CRITICAL**: A serious error, indicating that the program itself may be unable to continue running.

### Log output example

Note: To capture this sample output, I change the "threshold" value, that's why the disk usage is the same in both cases.

```log
2021-07-06 12:55:23,354: WARNING: NOT OK - Email alert has been sent - Partition: "/", Size: 250 GiB, Used: 2 GiB, Free: 235 GiB
2021-07-06 12:56:03,972: INFO: OK - Partition: "/", Size: 250 GiB, Used: 2 GiB, Free: 235 GiB
```

## Author

- [@JManzur](https://www.github.com/jmanzur)

## Documentation

- [Logging Module](https://docs.python.org/3/library/logging.html#module-logging)
- [PyYAML Module](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Google App Passwords](https://support.google.com/accounts/answer/185833?hl=en)