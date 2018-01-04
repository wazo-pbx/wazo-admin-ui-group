# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
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
        self._update_relations(resource)

    def _update_relations(self, group):
        members = group.get('members')
        fallbacks = group.get('fallbacks')
        schedules = group.get('schedules')

        if members:
            self._update_members_to_group(group, members)

        if fallbacks:
            self._update_fallbacks_to_group(group, fallbacks)

        if schedules:
            self._update_schedules_to_group(group, schedules)

    def _update_members_to_group(self, group, members):
        return confd.groups.relations(group).update_user_members(members.get('users'))

    def _update_fallbacks_to_group(self, group, fallbacks):
        return confd.groups.relations(group).update_fallbacks(fallbacks)

    def _update_schedules_to_group(self, group, schedules):
        existing_group = confd.groups.get(group)
        if existing_group['schedules']:
            schedule_id = existing_group['schedules'][0]['id']
            confd.groups(group).remove_schedule(schedule_id)
        if schedules[0].get('id'):
            confd.groups(group).add_schedule(schedules[0])

    def get_first_internal_context(self):
        result = confd.contexts.list(type='internal', limit=1, direction='asc', order='id')
        for context in result['items']:
            return context

    def get_context(self, context):
        result = confd.contexts.list(name=context)
        for context in result['items']:
            return context
