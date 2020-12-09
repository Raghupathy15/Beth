# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class HolidayMaster(models.Model):
	_name = "holiday.master"
	_description = "Holiday master"
	_inherit = 'mail.thread'

	name = fields.Char(string='Reason',required=True,track_visibility='always')
	date = fields.Date(string='Date', required=True,default=fields.Date.today())