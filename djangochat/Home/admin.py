from django.contrib import admin
from .models import Profile,Event,Club
# Register your models here.

admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Profile)