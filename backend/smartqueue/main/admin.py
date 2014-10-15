from django.contrib import admin
from models import *

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Vendor, VendorAdmin)


class QueueAdmin(admin.ModelAdmin):
    list_display = ('name','vendor', 'group_size')
admin.site.register(Queue, QueueAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'queue', 'reservation_number')
admin.site.register(Reservation, ReservationAdmin)