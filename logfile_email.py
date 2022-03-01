import os
import time
from datetime import datetime
import smtplib
import csv
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Function used to send the email with attachment
def email_routine(filedir,file,error_match):
    msg, attach = None,None
    
    title = error_dict[error_match][0]
    body = error_dict[error_match][1]
    to_addr = error_dict[error_match][2]
    
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")   
    
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = title + " " + dt_string
    
    with open(filedir, "r") as f:
        text = f.read()
        text_n = "\n".join(text.splitlines()[-textnum:])
        body = body + "\n\n" + text_n
        
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(text)
        encoders.encode_base64(attach)
    attach.add_header('Content-Disposition', 'attachment', filename=file)
        
    msg.attach(MIMEText(body, "plain"))
    msg.attach(attach)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        
    print("Email sent")
    
#Checks for new lines within each file
def new_line_check(recent_files,prev_data):
    new_data = {}

    for file in recent_files:
        try:
            with open(report_folder+file, errors='ignore') as f:
                text_list = set(frozenset(list(enumerate(f.read().splitlines()))[-30:]))
                new_data[file] = text_list
        except:
            continue

    if not prev_data:
        return {},new_data
    
    else:
        new_lines = {}
        for file in new_data:
            try:
                difference = new_data[file]-prev_data[file]
                if difference != set():
                    new_lines[file] = difference
                    difference_report = [i[1] for i in difference]
                    print(f"{file} has been modified: {difference_report}")
            except:
                print(f"New file created {file}")
                new_lines[file] = new_data[file]
            
    return new_lines, new_data

# Loads the different config files
folder = os.getcwd()+"\\"
config_file = folder+"config.txt"
error_file = folder+"error_types.csv"
config = eval(open(config_file,'r').read())

error_dict = {}
with open(error_file, newline="") as csvfile:
    data = csv.reader(csvfile, delimiter=",")
    for row in data:
        error_dict[row[0]] = row[1:] if len(row) > 1 else []
    
error_types = list(error_dict.keys())[1:]
report_folder = config["filedir"]+"\\"
from_addr = config["sender_email"]
password = config["password"]
textnum = int(config["textnum"])
wait_time = int(config["wait_time"])
new_data = {}
current_files = {}

# Runs the functions once to save all recent file content
file_list = set(os.listdir(report_folder))
recent_files = list(filter(lambda file : (time.time()-os.path.getmtime(report_folder+file))/3600 < 24,file_list))
if recent_files:
        new_lines, new_data = new_line_check(recent_files,new_data)
print("Looking for new error files...")

run = 1
while run:
    time.sleep(wait_time)
    file_list = set(os.listdir(report_folder))
    
    # This is the date filter
    recent_files = list(filter(lambda file : (time.time()-os.path.getmtime(report_folder+file))/3600 < 24,file_list))
    
    if recent_files:
        new_lines, new_data = new_line_check(recent_files,new_data)
            
        if new_lines:
            for file in new_lines.keys():
                error_match = [error for error in error_types if error in list(new_lines[file])[0][1]]
                if error_match:
                    print(f"Error matched {error_match}")
                    email_routine(report_folder+file,file,error_match[0])
