# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm

from wtforms.fields import (SubmitField,
                            FormField,
                            StringField,
                            SelectField,
                            SelectMultipleField,
                            BooleanField)
from wtforms.validators import InputRequired

from wazo_admin_ui.helpers.destination import FallbacksForm, DestinationHiddenField


class GroupForm(FlaskForm):
    name = StringField('Name', [InputRequired()])
    extension = StringField('Extension')
    users = SelectMultipleField('Members', choices=[])
    caller_id_mode = SelectField('Callerid mode', choices=[('prepend', 'Prepend')])
    caller_id_name = StringField('Callerid name')
    enabled = BooleanField('Enabled')
    music_on_hold = StringField('Music On Hold')
    preprocess_subroutine = StringField('Subroutine')
    retry_delay = StringField('Retry delay')
    ring_in_use = BooleanField('Ring in use')
    ring_strategy = SelectField('Ring strategy', choices=[('all', 'All')])
    timeout = StringField('Timeout')
    user_timeout = StringField('User timeout')
    fallbacks = FormField(FallbacksForm)
    submit = SubmitField('Submit')


class GroupDestinationForm(FlaskForm):
    setted_value_template = '{group_name}'

    group_id = SelectField('Group', choices=[])
    ring_time = StringField('Ring Time')
    group_name = DestinationHiddenField()
