# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm

from wtforms.fields import SubmitField
from wtforms.fields import TextField
from wtforms.fields import SelectField
from wtforms.fields import SelectMultipleField

from wtforms.validators import InputRequired

from wazo_admin_ui.helpers.destination import DestinationHiddenField


class GroupForm(FlaskForm):
    name = TextField('Name', [InputRequired()])
    extension = TextField('Extension')
    users = SelectMultipleField('Members', choices=[])
    submit = SubmitField('Submit')

class GroupDestinationForm(FlaskForm):
    setted_value_template = '{group_name}'

    group_id = SelectField('Group', choices=[])
    ring_time = TextField('Ring Time')
    group_name = DestinationHiddenField()
