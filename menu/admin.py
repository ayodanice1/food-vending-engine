from django.contrib import admin

from .menu_models.day import Day
from .models import Menu


# Register your models here.
admin.site.register(Day)
admin.site.register(Menu)
