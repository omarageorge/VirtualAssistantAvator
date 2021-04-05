from datetime import datetime

# Confirms hour  of the day
def checkTimeOfDay(greeting):
    # Create a time object
    time_str = datetime.now()
    
    # Retrieve current hour of the day
    hour_of_day = int(time_str.strftime('%H'))
    
    # Make comparison to identify correct response
    if hour_of_day < 12:
        return 'morning'
    elif hour_of_day >= 12 and hour_of_day < 18:
        return 'afternoon'
    else:
        return 'evening'