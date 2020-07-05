from .day import Day


opening_days = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
]

for opening_day in opening_days:
    try:
        day = Day(name=opening_day)
        day.save()
    except:
        continue
