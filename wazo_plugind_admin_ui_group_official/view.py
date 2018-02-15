# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_babel import lazy_gettext as l_
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import GroupForm


class GroupView(BaseView):
    form = GroupForm
    resource = 'group'

    @classy_menu_item('.groups', l_('Groups'), order=1, icon="users")
    def index(self):
        return super(GroupView, self).index()

    def _map_resources_to_form(self, resource):
        users = [user['uuid'] for user in resource['members']['users']]
        resource['members']['user_uuids'] = users
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(form.members.users)
        form.extensions[0].exten.choices = self._build_set_choices_exten(form.extensions[0])
        form.extensions[0].context.choices = self._build_set_choices_context(form.extensions[0])
        form.music_on_hold.choices = self._build_set_choices_moh(form.music_on_hold)
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(form.schedules[0])
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = '{} {}'.format(user.firstname.data, user.lastname.data)
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_internal_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        return [(moh.data, moh.data)]

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super(GroupView, self)._map_form_to_resources(form, form_id)
        resource['members']['users'] = [{'uuid': user_uuid} for user_uuid in form.members.user_uuids.data]
        return resource

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
