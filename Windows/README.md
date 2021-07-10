# Check Windows disk capacity and send an email alert

This simple Python script scans a given Windows drive (mount point) and, based on a specified percentage threshold, triggers an email notification that includes a detailed summary of the server and current disk usage. Also a log file is generated every time that the script is run.

## Tested with: 

| Environment | Application | Version  |
| ----------------- |-----------|---------|
| Windows 10 21H1 | Python | 3.9.5|

## How-To

Create a file called "mail_cred.yml" located in the root folder with a content similar to the following:

```bash
ADDRESS: 'sender@gmail.com'
PASSWORD: 'xxxxxxxxxxxxxxxxx'
SEND_TO: 'recipient@example.com'
#SEND_TO: 'one@example.com, two@example.com, three@example.com'
```
Install the necessaries python requirements, by runing:

```bash
pip3 install -r requirements.txt
```

Finally, set the variables "threshold" and the drive letter after the "if p.device ==" statement. 

![App Screenshot](https://1.bp.blogspot.com/-l7BJbeB9G9E/YOdhhVbUqLI/AAAAAAAAFoM/9xKW_l9YQiQjxUnOxYrGkKU_T1xPaW_awCLcBGAsYHQ/s16000/python-wda.png)

By doing that, you are all set. Now you can test the script:

```bash
python3 windows_disk_alert.py
```

And when you're ready go ahead and schedule a task in the "Windows Task Scheduler" to run it on a regular basis. In my case (because I'm using the PyYAML module to load the email credential), I'm calling a simple powershell script from crontab:

```powershell
cd C:\Scripts\Disk_Alert
python3 windows_disk_alert.py
```

```powershell
.\run_script.ps1
```

**IMPORTAM:** To run the powershell script you need to enable PowerShell Scripts Execution:


```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

An in the "Windows Task Scheduler" you need to specified the following argument:

- -ExecutionPolicy Bypass C:\Scripts\Disk_Alert\run_script.ps1

![App Screenshot](https://1.bp.blogspot.com/-rnB_jW0gjHo/YOn3QfC1s_I/AAAAAAAAFoU/b7JRSZeXxT4dn0kkK_7BYW0cfBNkTWFggCLcBGAsYHQ/s493/python-wda-task.png)

## Log file

Every time you run the script, a log file called "wdisk_alert.log" will be generated/updated with information similar to the following:

```log
2021-07-10 16:19:14,863: INFO: Drive: "C:\", Total Size: 237.23 GiB, Used: 108.06, Free: 129.17 GiB, Usage Percentage: 45.6%, File System: NTFS.
2021-07-10 16:19:14,863: INFO: OK - Drive "C:\" has a usage percentage less than the defined threshold of 10%
2021-07-10 16:19:46,168: WARNING: Drive: "C:\", Total Size: 237.23 GiB, Used: 108.06, Free: 129.17 GiB, Usage Percentage: 45.6%, File System: NTFS.
2021-07-10 16:19:46,169: WARNING: NOT OK - Email alert has been sent - Drive "C:\" has a usage percentage greater than the defined threshold of 50%
```

**Note**: To capture this sample output, I change the "threshold" value, that's why the disk usage is the same in both cases.

## Email Alert:

When the disk usage exceeds the specified threshold, an email alert will be sent with a content similar to the following:

![App Screenshot](https://1.bp.blogspot.com/-2p-1jk1L1Iw/YOoEKoQ96rI/AAAAAAAAFoc/tynbiiHkcTc0YBZFFQLA13XHfBml-sifwCLcBGAsYHQ/s16000/python-wmail.png)

**Note**: None of the values need to be hard-coded, each one (hostname, IP, threshold, and disk-related information) is generated automatically.

## Debugging / Troubleshooting:


#### **Known issue #1**: Error running with python3
 - **Issue**: If when you run the powershell script you get an error, change it to python instead of python3

## Author

- [@JManzur](https://www.github.com/jmanzur)

## Documentation

- [Logging Module](https://docs.python.org/3/library/logging.html#module-logging)
- [PyYAML Module](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Google App Passwords](https://support.google.com/accounts/answer/185833?hl=en)