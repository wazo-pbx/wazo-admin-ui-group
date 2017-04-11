# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import jsonify, request
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import GroupForm


class GroupView(BaseView):

    form = GroupForm
    resource = 'group'

    @classy_menu_item('.groups', 'Groups', order=1, icon="users")
    def index(self):
        return super(GroupView, self).index()

    def _map_resources_to_form(self, resource):
        users = [user['uuid'] for user in resource['members']['users']]
        form = self.form(data=resource, users=users)
        form.users.choices = self._build_setted_choices(resource['members']['users'])
        form.extensions[0].context.choices = self._build_setted_choices_context(resource.get('extensions'))
        form.music_on_hold.choices = self._build_setted_choices_moh(resource.get('music_on_hold'))
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

    def _build_setted_choices_moh(self, moh):
        return [(moh, moh)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('group', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form


class GroupDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [{'id': group['id'], 'text': group['name']} for group in groups['items']]
        return jsonify(build_select2_response(results, groups['total'], params))
