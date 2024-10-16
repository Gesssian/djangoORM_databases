from django.contrib import admin

from .models import *

admin.site.register(Climber)
admin.site.register(Expedition)
admin.site.register(ClimberExpedition)
