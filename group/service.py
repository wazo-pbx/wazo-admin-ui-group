# -*- coding: utf-8 -*-
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
        self._update_members(resource)

    def update(self, resource):
        super(GroupService, self).update(resource)
        self._update_members(resource)

    def _update_members(self, group):
        members = group.get('users')
        fallbacks = group.get('fallbacks')

        if members:
            self._update_members_to_group(group, self._generate_users(members))

        if fallbacks:
            self._update_fallbacks_to_group(group, fallbacks)

    def _update_members_to_group(self, group, members):
        return confd.groups.relations(group).update_user_members(members)

    def _update_fallbacks_to_group(self, group, fallbacks):
        return confd.groups.relations(group).update_fallbacks(fallbacks)

    def _generate_users(self, users):
        return [{'uuid': user} for user in users]
