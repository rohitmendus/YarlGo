from datetime import datetime, time

def is_time_between(begin_time, end_time, check_time):
    if begin_time < end_time:
        return check_time > begin_time and check_time < end_time
    else:
        return check_time > begin_time or check_time < end_time