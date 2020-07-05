from django.db import models


class Day(models.Model):
    name = models.CharField(
        max_length=3, 
        choices= (
            ('MON', 'Monday'),
            ('TUE', 'Tuesday'),
            ('WED', 'Wednesday'),
            ('THU', 'Thursday'),
            ('FRI', 'Friday'),
            ('SAT', 'Saturday') ), 
        default='Monday', 
        unique=True )
    
    def __str__(self):
        return self.name
