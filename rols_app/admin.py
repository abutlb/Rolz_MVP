from django.contrib import admin
from .models import Device, Ticket, TicketComment

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'device_type', 'model', 'assigned_to', 'date_assigned')
    list_filter = ('device_type', 'assigned_to')
    search_fields = ('serial_number', 'model', 'assigned_to__username')
    date_hierarchy = 'date_assigned'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'device', 'status', 'priority', 'created_by', 'created_at', 'assigned_to')
    list_filter = ('status', 'priority', 'created_at', 'assigned_to')
    search_fields = ('title', 'description', 'created_by__username', 'device__serial_number')
    date_hierarchy = 'created_at'

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('comment', 'ticket__title', 'user__username')
    date_hierarchy = 'created_at'