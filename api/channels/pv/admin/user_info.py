from django import forms

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from channels.pv.models import PVUserInfo

class PVUserInfoAdmin(ChannelModelAdmin):
  list_display = ["id", "get_email", "can_apply", "approved_by_virtual_meeting"]
  list_filter = ["can_apply", "approved_by_virtual_meeting"]
  fields = ["can_apply", "approved_by_virtual_meeting"]
  search_fields = [
    "user__email",
    "user__name"
  ]

  def get_queryset(self, *args, **kwargs):
    return super(PVUserInfoAdmin, self).get_queryset(*args, **kwargs).select_related("user")

  def get_model_perms(self, request):
    if request.user.channel.slug != "pv":
      return {"change": False, "add": False, "delete": False}
    return super(PVUserInfoAdmin, self).get_model_perms(request)

  def get_email(self, obj):
    return obj.user.email

  get_email.admin_order_field  = "email"
  get_email.short_description = "User email"

admin_site.register(PVUserInfo, PVUserInfoAdmin)
