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
    context = SelectField('Context', choices=[])
    users = SelectMultipleField('Members', choices=[])
    caller_id_mode = SelectField('Callerid mode', choices=[
                                                      ('', 'None'),
                                                      ('prepend', 'Prepend'),
                                                      ('overwrite', 'Overwrite'),
                                                      ('append', 'Append')
                                                  ])
    caller_id_name = StringField('Callerid name')
    enabled = BooleanField('Enabled')
    music_on_hold = SelectField('Music On Hold', choices=[])
    preprocess_subroutine = StringField('Subroutine')
    retry_delay = StringField('Retry delay')
    ring_in_use = BooleanField('Ring in use')
    ring_strategy = SelectField('Ring strategy', choices=[
                                                     ('all', 'All'),
                                                     ('random', 'Random'),
                                                     ('least_recent', 'Least recent'),
                                                     ('linear', 'Linear'),
                                                     ('fewest_calls', 'Fewest calls'),
                                                     ('memorized_round_robin', 'Memorized round robin'),
                                                     ('weight_random', 'Weight random')
                                                 ])
    timeout = StringField('Timeout')
    user_timeout = StringField('User timeout')
    fallbacks = FormField(FallbacksForm)
    submit = SubmitField('Submit')


class GroupDestinationForm(FlaskForm):
    setted_value_template = u'{group_name}'

    group_id = SelectField('Group', choices=[])
    ring_time = StringField('Ring Time')
    group_name = DestinationHiddenField()
