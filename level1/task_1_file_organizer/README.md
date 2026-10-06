# File Organizer Automation Tool

The task sheet describes a tool that scans a selected directory, detects file types, moves files into named folders, handles duplicate names, and keeps a log. fileciteturn0file0L47-L57

## Run

```powershell
python file_organizer.py "C:\Users\YourName\Downloads"
```

Or:

```powershell
python file_organizer.py
```

A CSV log is created after organization.

## Safety

Test first on a folder containing copies of files. Do not run it on a critical Windows/system directory.
