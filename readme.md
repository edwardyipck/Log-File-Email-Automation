# Log file Email Automation

This python script allows you to automatically send emails with the log file attached 
once a certain phrase appears in the recent logs. 
This could be used to detect when a program fails and outputs an error message in the logs.

By selecting a destination folder, the script will look at all files modified for any changes 
within the last 24 hours and search for the custom specified phrases set in error_types.csv.

## config.txt:
This is a python dictionary so only edit inside the quotations on the right hand side of the colon

 - filedir: The folder that you want to search in. Make sure not to remove the r : r"D:\folder\goes\here"
 - sender_email: The email to be used
 - password: Your email password
 - textnum: The number of tail lines to include from the log file in the email
 - wait_time: The number of seconds between each folder search

## error_types.csv:
This csv is used to define custom phrases, and set email recipients, email titles and body for each phrase

 - Error: The exact phrase to search for in the log files
 - Title: The email title to be created
 - Body: The body of the email
 - EmailTo: The email recipient
