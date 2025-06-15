## 🐕‍🦺 Doberman - File Integrity Monitoring System

Doberman is a lightweight File Intergrity Monitor (FIM) which runs at startup via Task Scheduler (user needs to add) and alters user of any changes to a base file.

### What It Does:
Stores the hashes of base files on database and on startup compare the database hash and current hash to determine if the file has been modified. If the files have been modified or deleted it will send an alert email to the user/authorities.
Workflow:
- Generate baseline hash and add them to database by running hash.py
- Update the database if any changes were made to the baseline files at any time
- Run alert script to compare the current hashes and recorded hashes
- (Option; Done by user) Add the code to Task Schedular to run on startup.


### Technologies Used:
- Python (hashlib, smtplib, psycopg2)
- PostgreSQL
- Windows Task Scheduler (Automation)


### How to Run:
1. Clone this repository
2. Install dependencies: 'pip install -r requirements.txt'
3. Run: 'hash_file.py'
4. Run: 'check_and_alert.py'
5. Add 'check_and_alert.py' to Windows Task Scheduler to run on startup (optional)


### Demo
YouTube: https://www.youtube.com/watch?v=FBCzDS2ffAs
