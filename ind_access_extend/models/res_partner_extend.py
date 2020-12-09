# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    customer_pan = fields.Char(string="PAN")
    phone = fields.Char(string='Mobile 1', required=True)
    mobile = fields.Char(string='Mobile 2')
    # state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', required=False, domain="[('country_id', '=?', country_id)]")n
    _sql_constraints = [('phone_uniq', 'unique (phone)', "Phone No already exists !")]
