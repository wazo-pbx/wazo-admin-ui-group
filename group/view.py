# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView, BaseDestinationView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, extract_form_fields

from wazo_admin_ui.helpers.destination import FallbacksSchema

from .form import GroupForm


class GroupSchema(BaseSchema):

    fallbacks = fields.Nested(FallbacksSchema)

    class Meta:
        fields = extract_form_fields(GroupForm)


class ExtensionSchema(BaseSchema):
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
        data = self.schema().load(resources).data
        users = [user['uuid'] for user in resources['group']['members']['users']]
        main_exten = schema.get_main_exten(resources['group'].get('extensions', {}))
        form = self.form(data=data['group'], extension=main_exten, users=users)
        form.users.choices = self._build_setted_choices(resources['group']['members']['users'])
        form.context.choices = self._build_setted_choices_context(resources['group'].get('extensions'))
        return form

    def _build_setted_choices(self, users):
        results = []
        for user in users:
            if user.get('lastname'):
                text = '{} {}'.format(user.get('firstname'), user['lastname'])
            else:
                text = user.get('firstname')
            results.append((user['uuid'], text))
        return results

    def _build_setted_choices_context(self, extensions):
        results = []
        for extension in extensions:
            if extension.get('context'):
                results.append((extension['context'], extension['context']))
        return results


class GroupDestinationView(BaseDestinationView):

    def list_json(self):
        params = self._extract_params()
        groups = self.service.list(**params)
        results = [{'id': group['id'], 'text': group['name']} for group in groups['items']]
        return self._select2_response(results, groups['total'], params)
