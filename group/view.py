# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView, BaseDestinationView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, extract_form_fields

from .form import GroupForm


class GroupSchema(BaseSchema):

    class Meta:
        fields = extract_form_fields(GroupForm)


class ExtensionSchema(BaseSchema):
    context = fields.String(default='default')
    exten = fields.String(attribute='extension')


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'group'

    group = fields.Nested(GroupSchema)
    extension = fields.Nested(ExtensionSchema)


class GroupView(BaseView):

    form = GroupForm
    resource = 'group'
    schema = AggregatorSchema

    @classy_menu_item('.groups', 'Groups', order=1, icon="users")
    def index(self):
        return super(GroupView, self).index()

    def _map_resources_to_form(self, resources):
        schema = self.schema()
        users = [user['uuid'] for user in resources['group']['members']['users']]
        main_exten = schema.get_main_exten(resources['group'].get('extensions', {}))
        return self.form(data=resources['group'], extension=main_exten, users=users)


class GroupDestinationView(BaseDestinationView):

    def list_json(self):
        return self._list_json('id')

    def uuid_list_json(self):
        return self._list_json('uuid')

    def _list_json(self, field_id):
        params = self._extract_params()
        groups = self.service.list(**params)
        results = []
        for group in groups['items']:
            text = '{}'.format(group['name'])
            results.append({'id': group[field_id], 'text': text})

        return self._select2_response(results, groups['total'], params)
