from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	service_id = fields.Many2one('tickets', string="Name",readonly=True)

	def action_availability_check(self):
		self.write({'state': 'customer_approval'})

	def action_customer_approval(self):
		self.action_confirm()
		self.write({'state': 'sale'})

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	# def _compute_service_id(self):
	# 	for line in self:
	# 		if line.order_id.service_id:
	# 			line.from_service = True
	# 		else:
	# 			line.from_service = False

	from_service = fields.Boolean('From Service')