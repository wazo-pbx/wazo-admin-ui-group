# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.service import BaseConfdService


class GroupService(BaseConfdService):

    resource_name = 'group'
    resource_confd = 'groups'
