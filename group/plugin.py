# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.core.destination import destination_blueprint

from .service import GroupService
from .view import GroupView, GroupDestinationView

group = create_blueprint('group', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        GroupView.service = GroupService(config['confd'])
        GroupView.register(group, route_base='/groups')
        register_flaskview(group, GroupView)

        GroupDestinationView.service = GroupService(config['confd'])
        GroupDestinationView.register(destination_blueprint, route_base='/group_destination')

        core.register_blueprint(group)
