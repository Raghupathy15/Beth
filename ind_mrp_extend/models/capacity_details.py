from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CapacityDetails(models.Model):
	_name = 'capacity.details'
	_inherit = ['mail.thread']
	_description = "Capacity Details"

	capacity = fields.Integer(string="Capacity per day",required=True, track_visibility='always')
	capacity_change = fields.Integer(string="Capacity per day")
	is_capacity = fields.Boolean(string="Capacity per day")

	@api.onchange('capacity')
	def onchange_capacity(self):
		if self.capacity:
			mrp = self.env['mrp.production'].sudo().search([('tentative_date','>=',fields.date.today())])
			if mrp:
				for production in mrp:
					mrp.tentative_date = False
			self.capacity_change = self.capacity
			self.is_capacity = True

	@api.constrains('capacity')
	def validations(self):
		if self.capacity and self.capacity < 0:
			raise UserError(_("Capacity should be greater than zero."))
		return True