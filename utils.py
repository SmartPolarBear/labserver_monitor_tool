import datetime

def seconds(hour,minutes,secs):
    return hour*3600+minutes*60+secs

def at_sleep_time(begin_hour,end_hour)->bool:
    nowtime= datetime.datetime.now()
    return nowtime.hour>begin_hour and nowtime.hour<end_hour