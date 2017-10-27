from django import forms
from django.contrib import admin

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import TabularInline
from ovp.apps.users.models import User
from channels.pv.models import PVMeeting
from channels.pv.models import PVMeetingAppointment

class PVMeetingAppointmentForm(forms.ModelForm):
  can_apply = forms.BooleanField(initial=False, required=False)

  def __init__(self, *args, **kwargs):
    super(PVMeetingAppointmentForm, self).__init__(*args, **kwargs)
    if 'instance' in kwargs:
      self.fields['can_apply'].initial = kwargs['instance'].user.pvuserinfo.can_apply
    else:
      self.fields['user'].required = False

  def save(self, commit=True):
    can_apply = self.cleaned_data.get('can_apply', False)
    self.cleaned_data['user'].pvuserinfo.can_apply = can_apply
    self.cleaned_data['user'].pvuserinfo.save()
    return super(PVMeetingAppointmentForm, self).save(commit=commit)

  class Meta:
    model = PVMeetingAppointment
    fields = "__all__"

class PVMeetingAppointmentInline(TabularInline):
  model = PVMeetingAppointment
  form = PVMeetingAppointmentForm
  fields = ['user', 'can_apply']

class PVMeetingAdmin(ChannelModelAdmin):
  list_display = ['id', 'date']
  fields = ['date', 'address','published', 'max_appointments']
  inlines = [
    PVMeetingAppointmentInline
  ]

  def get_model_perms(self, request):
    if request.user.channel.slug != "pv":
      return {'change': False, 'add': False, 'delete': False}
    return super(PVMeetingAdmin, self).get_model_perms(request)

admin_site.register(PVMeeting, PVMeetingAdmin)
