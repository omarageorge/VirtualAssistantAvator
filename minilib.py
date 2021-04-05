from datetime import datetime


# Create a time object
time_str = datetime.now()
    
# Retrieve current hour of the day
hour_of_day = int(time_str.strftime('%H'))
    
# check morning 
def isMorning():
    return True if hour_of_day < 12 else False

# check noon 
def isAfterNoon():
    return True if hour_of_day >= 12 and hour_of_day < 18 else False

# check evening
def isEvening():
    return True if hour_of_day >= 18 else False
