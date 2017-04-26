# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import (SubmitField,
                            FieldList,
                            FormField,
                            StringField,
                            SelectField,
                            SelectMultipleField,
                            BooleanField)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_admin_ui.helpers.destination import FallbacksForm, DestinationHiddenField
from wazo_admin_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = StringField('Extension')
    context = SelectField('Context', choices=[])


class GroupForm(BaseForm):
    name = StringField('Name', [InputRequired(), Length(max=128)])
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    users = SelectMultipleField('Members', choices=[])
    caller_id_mode = SelectField('Callerid mode', choices=[
                                                      ('', 'None'),
                                                      ('prepend', 'Prepend'),
                                                      ('overwrite', 'Overwrite'),
                                                      ('append', 'Append')
                                                  ])
    caller_id_name = StringField('Callerid name', [Length(max=80)])
    enabled = BooleanField('Enabled')
    music_on_hold = SelectField('Music On Hold', [Length(max=128)], choices=[])
    preprocess_subroutine = StringField('Subroutine', [Length(max=39)])
    retry_delay = IntegerField('Retry delay', [NumberRange(min=0)])
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
    timeout = IntegerField('Timeout', [NumberRange(min=0)])
    user_timeout = IntegerField('User timeout', [NumberRange(min=0)])
    fallbacks = FormField(FallbacksForm)
    submit = SubmitField('Submit')


class GroupDestinationForm(BaseForm):
    setted_value_template = u'{group_name}'

    group_id = SelectField('Group', [InputRequired()], choices=[])
    ring_time = IntegerField('Ring Time', [NumberRange(min=0)])
    group_name = DestinationHiddenField()
