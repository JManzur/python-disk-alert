# Check linux disk capacity and send an email alert

This simple Python script scans a given linux disk (mount point path) and, based on a specified percentage threshold, triggers an email notification that includes a detailed summary of the server and current disk usage. Also a log file is generated every time that the script is run.

## Tested with: 

| Environment | Application | Version  |
| ----------------- |-----------|---------|
| Windows 10 21H1 | Python | 3.9.5|


Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```powershell
cd C:\Scripts\Disk_Alert
python3 windows_disk_alert.py
```

Enable PowerShell Scripts Execution

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

```powershell
.\run_script.ps1
```