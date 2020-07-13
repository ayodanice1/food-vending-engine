def getDayFromDate( date_obj ):
    import datetime

    days = { 
        'Mon':'Monday', 
        'Tue':'Tuesday', 
        'Wed':'Wednesday', 
        'Thu':'Thursday', 
        'Fri':'Friday', 
        'Sat':'Saturday', 
    }
    # Get date string. E.g. Fri May 00:00:00 2020
    date_string = date_obj.ctime()
    day_abbr = date_string.split()[0]
    return days[day_abbr]

def itemCanBeOrderedOnOrderDueDay( item, order_due_day ):
    for day in item.scheduled_days.all():
        if order_due_day == str(day.name):
            return True
    return False
    
