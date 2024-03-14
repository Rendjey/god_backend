import os
import datetime
#The file contains the functions necessary for logging the project.

def dirs():
    current_datetime = datetime.datetime.now()
    date_log = current_datetime.strftime("%d_%m_%Y")

    try:
        os.mkdir("/home/flaskapp/logs/logs_" + date_log)
    except OSError as e:
        access = "ok"

    

    return 0

def main():
    dirs()
    return 0

main()