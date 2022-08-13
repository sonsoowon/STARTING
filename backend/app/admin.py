from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register([Club, Manager, Recruit, Apply, Comment, Notice, TimeTable, SelectTime, ApplyForm])