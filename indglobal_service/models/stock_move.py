from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class StockMove(models.Model):
	_inherit = "stock.move"

	warranty_months = fields.Char(string="Warranty Months")
	warranty_from = fields.Date(string="Warranty From")
	warranty_to = fields.Date(string="Warranty To")

class SaleOrder(models.Model):
	_inherit = "sale.order"

	def action_confirm(self):
		super(SaleOrder, self).action_confirm()
		for rec in self.order_line:
			pick = self.env['stock.picking'].search([('origin', '=',self.name)])
			if pick:
				for move in pick.move_ids_without_package:
					if move.product_id.warranty_months > 0:
						move.warranty_months = move.product_id.warranty_months
						move.warranty_from = datetime.today()
						warranty = move.warranty_from + relativedelta(months=move.product_id.warranty_months)
						move.warranty_to = warranty - relativedelta(days=1)
					else:
						move.warranty_months = move.product_id.warranty_months
						move.warranty_from = ''
						move.warranty_to = ''