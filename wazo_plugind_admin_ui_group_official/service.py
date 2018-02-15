# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdExtensionService
from wazo_admin_ui.helpers.confd import confd


class GroupService(BaseConfdExtensionService):

    resource_confd = 'groups'

    def create(self, resource):
        resource_created = super(GroupService, self).create(resource)
        resource['id'] = resource_created['id']
        del resource['fallbacks']
        self._update_relations(resource)

    def update(self, resource):
        super(GroupService, self).update(resource)
        existing_group = confd.groups.get(resource)
        self._update_relations(resource, existing_group)

    def _update_relations(self, group, existing_group=None):
        members = group.get('members')
        fallbacks = group.get('fallbacks')
        schedules = group.get('schedules')
        call_permissions = group.get('call_permissions')

        if members:
            self._update_members_to_group(group, members)

        if fallbacks:
            self._update_fallbacks_to_group(group, fallbacks)

        if schedules:
            self._update_schedules_to_group(group, schedules, existing_group)

        if call_permissions:
            self._update_callpermissions_relations(group, call_permissions, existing_group)

    def _update_members_to_group(self, group, members):
        return confd.groups.relations(group).update_user_members(members.get('users'))

    def _update_fallbacks_to_group(self, group, fallbacks):
        return confd.groups.relations(group).update_fallbacks(fallbacks)

    def _update_schedules_to_group(self, group, schedules, existing_group):
        if existing_group and existing_group.get('schedules'):
            schedule_id = existing_group['schedules'][0]['id']
            confd.groups(group).remove_schedule(schedule_id)
        if schedules[0].get('id'):
            confd.groups(group).add_schedule(schedules[0])

    def _update_callpermissions_relations(self, group, call_permissions, existing_group):
        if existing_group and existing_group.get('call_permissions'):
            call_permission_id = existing_group['call_permissions'][0]['id']
            confd.groups(group).remove_call_permission(call_permission_id)

        if call_permissions[0].get('id'):
            confd.groups(group).add_call_permission(call_permissions[0])

    def get_first_internal_context(self):
        result = confd.contexts.list(type='internal', limit=1, direction='asc', order='id')
        for context in result['items']:
            return context

    def get_context(self, context):
        result = confd.contexts.list(name=context)
        for context in result['items']:
            return context
