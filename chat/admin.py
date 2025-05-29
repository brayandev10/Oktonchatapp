from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.admin import AdminSite

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'value', 'file', 'date', 'read')
    list_filter = ('room', 'user', 'read')
    search_fields = ('value', 'user__username')


admin.site.site_header = "Administration CodeZone"
admin.site.site_title = "CodeZone Admin"
admin.site.index_title = "Bienvenue sur l'administration de CodeZone"

admin.site.register(Message, MessageAdmin)
admin.site.register(UserProfile)
admin.site.register(Room)