from django.contrib import admin
from .models import profileModel,Information

class profileAdmin(admin.ModelAdmin):
    list_display = ['user', 'contactNumber', ]

admin.site.register(profileModel, profileAdmin)
admin.site.register(Information)
