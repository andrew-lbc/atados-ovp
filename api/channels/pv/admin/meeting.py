from django import forms
from django.contrib import admin

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import TabularInline
from ovp.apps.users.models import User
from channels.pv.models import PVMeeting
from channels.pv.models import PVMeetingAppointment

class PVMeetingAppointmentInline(TabularInline):
  model = PVMeetingAppointment
  fields = ['user']

class PVMeetingAdmin(ChannelModelAdmin):
  list_display = ['id', 'date']
  fields = ['date']
  inlines = [
    PVMeetingAppointmentInline
  ]


admin_site.register(PVMeeting, PVMeetingAdmin)