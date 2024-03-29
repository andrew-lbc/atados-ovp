# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-03 08:41
from __future__ import unicode_literals

from django.db import migrations

from ovp.apps.core.helpers import generate_slug

def foward_func(apps, schema_editor):
    Channel = apps.get_model("channels", "Channel")
    channel = Channel.objects.create(name="Boehringer", slug="boehringer")

    # We freeze default channels skills and causes because
    # post_save signals are not sent from migrations
    from ovp.apps.core.models.skill import skills
    from ovp.apps.core.models.cause import causes

    Skill = apps.get_model("core", "Skill")
    Cause = apps.get_model("core", "Cause")

    for skill in skills:
      skill = Skill.objects.create(name=skill, channel=channel)
      skill.slug = generate_slug(Skill, skill.name, skill.channel.slug)
      skill.save()

    for cause in causes:
      cause = Cause.objects.create(name=cause, channel=channel)
      cause.slug = generate_slug(Cause, cause.name, cause.channel.slug)
      cause.save()


    # Create channel settings
    ChannelSetting = apps.get_model("channels", "ChannelSetting")
    ChannelSetting.objects.create(key="MAPS_API_LANGUAGE", value="pt-br", channel=channel)
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="volunteerUnapplied-toOwner", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvited-toMemberInviter", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvited-toOwner", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvited-toOwnerInviter", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvitedRevoked-toMemberInviter", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvitedRevoked-toOwner", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvitedRevoked-toOwnerInviter", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userInvitedRevoked-toUser", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userJoined-toUser", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userLeft-toOwner", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userLeft-toUser", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userRemoved-toOwner", channel=channel)
    ChannelSetting.objects.create(key="DISABLE_EMAIL", value="userRemoved-toUser", channel=channel)


def rewind_func(apps, schema_editor):
    return True

class Migration(migrations.Migration):

    dependencies = [
        ('default', '0001_initial'),
        ('channels', '0008_channel_subchannels'),
        ('core', '0021_auto_20171005_1902')
    ]

    operations = [
        migrations.RunPython(foward_func, rewind_func)
    ]
