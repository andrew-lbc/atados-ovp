from django import forms

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from channels.pv.models import PVUserInfo

class PVUserInfoAdmin(ChannelModelAdmin):
  list_display = ['id', 'get_email', 'can_apply']
  fields = ['can_apply']
  search_fields = [
    'user__email'
  ]

  def get_email(self, obj):
    return obj.user.email

  get_email.admin_order_field  = 'email'
  get_email.short_description = 'User email'

admin_site.register(PVUserInfo, PVUserInfoAdmin)
