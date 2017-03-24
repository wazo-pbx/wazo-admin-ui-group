# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdExtensionService


class GroupService(BaseConfdExtensionService):

    resource_name = 'group'
    resource_confd = 'groups'


    def create(self, resources):
        resource = super(GroupService, self).create(resources)
        self._update_members(resources, resource)

    def update(self, resources):
        super(GroupService, self).update(resources)
        self._update_members(resources)

    def _update_members(self, resources, resource=None):
        group = resources.get(self.resource_name)
        members = group.get('users')
        fallbacks = group.get('fallbacks')

        if resource == None:
            resource = group['id']

        if members:
            self._update_members_to_group(resource, self._generate_users(members))

        if fallbacks:
            self._update_fallbacks_to_group(resource, fallbacks)

    def _update_members_to_group(self, group, members):
        return self._confd.groups.relations(group).update_user_members(members)

    def _update_fallbacks_to_group(self, group, fallbacks):
        return self._confd.groups.relations(group).update_fallbacks(fallbacks)

    def _generate_users(self, users):
        return [{'uuid': user} for user in users]
