# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_destination_form, register_listing_url
from wazo_admin_ui.helpers.funckey import register_funckey_destination_form

from .service import GroupService
from .view import GroupView, GroupDestinationView
from .form import GroupDestinationForm, GroupFuncKeyDestinationForm

group = create_blueprint('group', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        GroupView.service = GroupService()
        GroupView.register(group, route_base='/groups')
        register_flaskview(group, GroupView)

        GroupDestinationView.service = GroupService()
        GroupDestinationView.register(group, route_base='/group_destination')

        register_destination_form('group', l_('Group'), GroupDestinationForm)
        register_funckey_destination_form('group', l_('Group'), GroupFuncKeyDestinationForm)
        register_listing_url('group', 'group.GroupDestinationView:list_json')

        core.register_blueprint(group)
