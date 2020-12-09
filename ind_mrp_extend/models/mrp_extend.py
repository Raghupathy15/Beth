# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError


class MrpProductionInherit(models.Model):
	""" Manufacturing Orders """
	_inherit = 'mrp.production'
	_description = 'Production Order'


	availability = fields.Boolean("Availabity Checked")
	state = fields.Selection([
		('draft', 'Draft'),
		('confirmed', 'New Entry  '),
		('design_stage', 'Design Stage'),
		('ready_for_punching', 'Ready For Punching'),
		('punching_done', 'Punching Done'),
		('bending_done', 'Bending Done'),
		('sub_assembly', 'Sub Assembly'),
		('coloring_set', 'Coloring to be set'),
		('coloring_sent', 'Coloring sent'),
		('color_sent', 'Coloring sent'),
		('coloring_completed', 'Coloring Completed'),
		('final_assembly', 'Final Assembly'),
		('quality_approved', 'Quality Approved'),
		('fg_credited', 'FG Credited'),
		('desp', 'Despatched'),
		('installation', 'Installation'),
		# ('installtion_completed', 'Installation Completed'),
		# ('warranty_card', 'Warranty Card'),
		('planned', 'Planned'),
		('progress', 'In Progress'),
		('to_close', 'Installation Completed'),
		('done', 'Warranty Card'),
		('cancel', 'Cancelled')], string='Status',
		compute='_compute_state', store=True, copy=False, index=True, readonly=True,
		tracking=True,
		help=" * Draft: The MO is not confirmed yet.\n"
			 " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
			 " * Planned: The WO are planned.\n"
			 " * In Progress: The production has started (on the MO or on the WO).\n"
			 " * To Close: The production is done, the MO has to be closed.\n"
			 " * Done: The MO is closed, the stock moves are posted. \n"
			 " * Cancelled: The MO has been cancelled, can't be confirmed anymore.")

	@api.depends('origin')
	def _compute_sale_order(self):
		is_finance_acc_manager = self.env.user.has_group('ind_access_extend.group_finance_account_manager_admin')
		is_finance_executive = self.env.user.has_group('ind_access_extend.group_finance_executive_admin')
		is_finance_head = self.env.user.has_group('ind_access_extend.group_finance_head_admin')
		if is_finance_acc_manager or is_finance_executive or is_finance_head:
			self.is_finance_group = True
		else:
			self.is_finance_group = False
		for mrp_origin in self:
			if mrp_origin.origin:
				# sale_ref = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
				for sale_ref in self.env['sale.order'].sudo().search([('name', '=', mrp_origin.origin)]):
					if sale_ref:
						mrp_origin.order_id = sale_ref.id
						mrp_origin.sum_total_dp = sale_ref.sum_total_dp
					else:
						mrp_origin.order_id = False
						mrp_origin.sum_total_dp = False
			else:
				mrp_origin.order_id = False
				mrp_origin.sum_total_dp = False


	is_finance_group = fields.Boolean("Is Finance", compute="_compute_sale_order")
	order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
							   copy=False, compute='_compute_sale_order')
	sap_sale_no = fields.Char('SAP Sale Order Number', related="order_id.sap_sale_no")
	sap_file = fields.Binary('SAP Sale Order File', help="Upload File", related="order_id.sap_file")
	sap_file_name = fields.Char('File Name from payment', related="order_id.sap_file_name")
	national_head_id = fields.Many2one("res.users", string="National Head", related="order_id.national_head_id")
	regional_bdm_id = fields.Many2one("res.users", string="RM Direct", related="order_id.regional_bdm_id")
	bdm_id = fields.Many2one("res.users", string="BDM Direct", related="order_id.bdm_id")
	blpl_service_manager_id = fields.Many2one("res.users", string='BLPL Service Manager',
											  related="order_id.blpl_service_manager_id")
	blpl_service_engineer_id = fields.Many2one("res.users", string='Service Engineer',
											   related="order_id.blpl_service_engineer_id")
	blpl_master_id = fields.Many2one("blpl.master", string="Bethliving Store Profile",
									 related="order_id.blpl_master_id")
	blpl_store_team_id = fields.Many2one("res.users", string="BLPL Store Team",
										 related="order_id.blpl_store_team_id")
	interior_consultant_id = fields.Many2one("res.users", string="Interior Consoultants",
											 related="order_id.interior_consultant_id")
	sales_team_lead_id = fields.Many2one("res.users", string="Sales Team Lead",
										 related="order_id.sales_team_lead_id")
	sales_lead_id = fields.Many2one("res.users", string="Sales Lead", related="order_id.sales_lead_id")
	blpl_service_techinician_id = fields.Many2one("res.users", string="Service Techinician",
												  related="order_id.blpl_service_techinician_id")

	deal_associate_id = fields.Many2one("res.users", string="Dealer", related="order_id.deal_associate_id")
	blpl_associate_id = fields.Many2one("res.users", string="Associates", related="order_id.blpl_associate_id")
	# Franchisee
	franchisee_national_head_id = fields.Many2one("res.users", string="National Head",
												  related="order_id.franchisee_national_head_id")
	franchisee_rm_id = fields.Many2one('res.users', string='RM', related="order_id.franchisee_rm_id")
	franchisee_bdm_id = fields.Many2one('res.users', string='BDM', related="order_id.franchisee_bdm_id")
	franchisee_blpl_service_manager_id = fields.Many2one(comodel_name="res.users", string="BLPL Service Manager",
														 related="order_id.franchisee_blpl_service_manager_id")
	franchisee_blpl_service_engineer_id = fields.Many2one(comodel_name="res.users", string="Service Engineer",
														  related="order_id.franchisee_blpl_service_engineer_id")

	franchisee_master_id = fields.Many2one("franchisee.master", string="Franchisee Profile",
										   related="order_id.franchisee_master_id")
	franchisee_owner_id = fields.Many2one("res.users", string="Franchisee Owner",
										  related="order_id.franchisee_owner_id")

	sales_cordinators_id = fields.Many2one('res.users', string='Sales Cordinator',
										   related="order_id.sales_cordinators_id")

	sales_managere_id = fields.Many2one(comodel_name="res.users",
										string="Sales Manager", related="order_id.sales_managere_id")
	sales_executive_id = fields.Many2one(comodel_name="res.users",
										 string="Sales Executive", related="order_id.sales_executive_id")
	service_technician_id = fields.Many2one(comodel_name="res.users",
											string="Service Techinician",
											related="order_id.service_technician_id")
	franchisee_dealer_id = fields.Many2one(comodel_name="res.users", string="Dealer",
										   related="order_id.franchisee_dealer_id")
	associates_id = fields.Many2one(comodel_name="res.users",
									string="Associates", related="order_id.associates_id")

	@api.depends('sap_code_sale')
	def _sap_code_compute(self):
		for rec in self:
			if rec.sap_code_sale:
				rec.sap_code_sale_char = rec.sap_code_sale
			else:
				rec.sap_code_sale_char = ''


# End Franchisee

	progress = fields.Float("Progress", compute='_compute_progress_hours', store=True, group_operator=False,
							help="Display progress of current task.")

	product_group_id = fields.Many2one('product_group.master',string="Product Group",readonly=True)
	checklist_ids = fields.One2many('product.checklist','header_id',string='Product Checklist')
	# finance_team = fields.Selection([('approve', 'Approve'),('not_approve', 'Not Approve')], string="Finance Team Approve for Manufacturing", tracking=True, default='not_approve')
	# finance_head = fields.Selection([('approve', 'Approve'),('not_approve', 'Not Approve')], string="Finance Head Approve for Manufacturing", tracking=True,)
	finance_team_desp = fields.Selection([('approve', 'Approve'), ('not_approve', 'Not Approve')],
									string="Finance Team Approve for Despatch", tracking=True, default='not_approve')
	install_completed_dealer = fields.Selection([('approve', 'Approve'), ('not_approve', 'Not Approve')],
										 string="Dealer Approve for Installation", tracking=True, default='not_approve')
	install_completed_customer = fields.Selection([('approve', 'Approve'), ('not_approve', 'Not Approve')],
										 string="Customer Approve for Installation", tracking=True, default='not_approve')
	company_branch_type = fields.Selection([
		('direct_store', 'Direct Store'),
		('franchisee', 'Franchisee')], string='Company Type', related='company_id.company_branch_type')



	sap_code_sale = fields.Integer('Sap Code', related='product_id.product_code')
	sap_code_sale_char = fields.Char('Sap Code', compute='_sap_code_compute')
	description_sale =	fields.Text('Description', related='product_id.description_sale')
	dealer_id = fields.Many2one('res.partner', string="Customer", store=True, related='order_id.dealer_id')
	partner_id = fields.Many2one('res.partner', string="Store Name", store=True, related='order_id.partner_id')
	sum_total_dp = fields.Float(string='Total DP', store=True, compute='_compute_sale_order',  group_operator=False)
	type_of_order = fields.Selection(
		[('express', 'Express'), ('standard', 'Standard'), ('lightning', 'Lightning'), ('token', 'Token')],
		string="Type Of Order", related='order_id.type_of_order')
	sale_date_order = fields.Datetime("Sales Order Approved Date", index=True, related="order_id.date_order")
	fg_credited_date = fields.Date("Fg Credited Date")

	mrp_queue_no = fields.Integer('Queue No',default='0', group_operator=False)
	mrp_queue_no_change = fields.Integer('Queue No Change',default='0')
	tentative_date = fields.Date('Tentative delivery date',readonly=True)

	def _cron_queue_no_creation(self):
		mrp = self.env['mrp.production'].search([])
		mrp.action_queue_no_creation()
		mrp.action_tentative_date_creation()

	def action_tentative_date_creation(self):
		capacity_details = self.env['capacity.details'].search([])
		mrp = self.env['mrp.production'].sudo().search([('tentative_date','=',False)],order="mrp_queue_no asc")
		check_last_date = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="mrp_queue_no desc",limit=1)
		if capacity_details and mrp:
			if check_last_date:
				print ('1111111111111111')
				for data in mrp:
					print ('22222222222222222',data)
					check_lst_date = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="mrp_queue_no desc",limit=1)
					if capacity_details.capacity_change == 0:
						capacity_details.capacity_change = capacity_details.capacity
						lst_date = check_lst_date.tentative_date
						tentative_date = lst_date + timedelta(days=+1)
						holiday_master = self.env['holiday.master'].sudo().search([('date','=',tentative_date)])
						if holiday_master:
							data.tentative_date = holiday_master.date + timedelta(days=+1)
						else:
							print ('3333333333333333')
							data.tentative_date = lst_date + timedelta(days=+1)
						capacity_details.is_capacity = True
					if not capacity_details.capacity_change == 0 and capacity_details.is_capacity == True:
						print ('3333333333333333')
						last = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="mrp_queue_no desc",limit=1)
						last_date=last.tentative_date
						data.tentative_date = last_date
						capacity_details.capacity_change = capacity_details.capacity_change-1
						if capacity_details.capacity_change == 0:
							capacity_details.is_capacity = False
			else:
				print ('4444444444444444444')
				mrp_rec = self.env['mrp.production'].sudo().search([('tentative_date','=',False)],order="mrp_queue_no asc",limit=1)
				print ('aaaaaaaaaaaaaaaaa',mrp_rec)
				if mrp_rec:
					mrp_rec.tentative_date = fields.date.today()
					capacity_details.capacity_change = capacity_details.capacity_change-1
		return True

	# def action_tentative_date_creation(self):
	# 	from datetime import date,timedelta
	# 	capacity_details = self.env['capacity.details'].search([])
	# 	mrp = self.env['mrp.production'].sudo().search([('tentative_date','=',False)],order="id asc")
	# 	check_last_date = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="id desc",limit=1)
	# 	if mrp:
	# 		if check_last_date:
	# 			for data in mrp:
	# 				check_lst_date = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="id desc",limit=1)
	# 				if capacity_details.capacity_change == 0:
	# 					capacity_details.capacity_change = capacity_details.capacity
	# 					lst_date = check_lst_date.tentative_date
	# 					tentative_date = lst_date + timedelta(days=+1)
	# 					holiday_master = self.env['holiday.master'].sudo().search([('date','=',tentative_date)])
	# 					if holiday_master:
	# 						data.tentative_date = holiday_master.date + timedelta(days=+1)
	# 					else:
	# 						data.tentative_date = lst_date + timedelta(days=+1)
	# 					capacity_details.is_capacity = True
	# 				if not capacity_details.capacity_change == 0 and capacity_details.is_capacity == True:
	# 					last = self.env['mrp.production'].sudo().search([('tentative_date','!=',False)],order="id desc",limit=1)
	# 					last_date=last.tentative_date
	# 					data.tentative_date = last_date
	# 					capacity_details.capacity_change = capacity_details.capacity_change-1
	# 					if capacity_details.capacity_change == 0:
	# 						capacity_details.is_capacity = False
	# 		else:
	# 			mrp_rec = self.env['mrp.production'].sudo().search([('tentative_date','=',False)],order="id asc",limit=1)
	# 			if mrp_rec:
	# 				mrp_rec.tentative_date = fields.date.today()
	# 				capacity_details.capacity_change = capacity_details.capacity_change-1
	# 	return True

	def action_queue_no_creation(self):
		origin = []
		for new_mrp in self.env['mrp.production'].sudo().search([('mrp_queue_no','=',0)]):
			if new_mrp and new_mrp.mrp_queue_no == 0:
				seq = self.env['mrp.production'].sudo().search([('mrp_queue_no','>',-1)],order="mrp_queue_no desc",limit=1)
				if seq:
					new_mrp.mrp_queue_no = seq.mrp_queue_no+1
					new_mrp.mrp_queue_no_change = new_mrp.mrp_queue_no
					origin.append(new_mrp.origin)
					multi_records = self.env['mrp.production'].sudo().search([('origin','=',new_mrp.origin)])
					if multi_records:
						for multi in multi_records:
							multi.mrp_queue_no = new_mrp.mrp_queue_no
							multi.mrp_queue_no_change = multi.mrp_queue_no
		return True

	@api.onchange('mrp_queue_no')
	def onchange_mrp_queue_no(self):
		if self.mrp_queue_no:
			duplicate = self.env['mrp.production'].sudo().search([('origin','=',self.origin)])
			if duplicate:
				for rec in duplicate:
					rec.mrp_queue_no = self.mrp_queue_no
					rec.mrp_queue_no_change = self.mrp_queue_no
			if self.mrp_queue_no_change < self.mrp_queue_no:
				smaller_records = self.env['mrp.production'].sudo().search([('mrp_queue_no','<=',self.mrp_queue_no),('mrp_queue_no','>',self.mrp_queue_no_change),('origin','!=',rec.origin)])
				if smaller_records:
					for small in smaller_records:
						small.mrp_queue_no = small.mrp_queue_no - 1
						small.mrp_queue_no_change = small.mrp_queue_no
			if self.mrp_queue_no_change > self.mrp_queue_no:
				bigger_records = self.env['mrp.production'].sudo().search([('mrp_queue_no','>=',self.mrp_queue_no),('mrp_queue_no','<',self.mrp_queue_no_change),('origin','!=',rec.origin)])
				if bigger_records:
					for bigger in bigger_records:
						bigger.mrp_queue_no = bigger.mrp_queue_no + 1
						bigger.mrp_queue_no_change = bigger.mrp_queue_no

	def action_confirm(self):
		for data in self:
			if not data.product_group_id:
				data.product_group_id = data.product_id.product_group_id.id
			for rec in data.product_group_id:
				for vals in self.env['questions.master'].sudo().search([('product_group_id', '=', data.product_group_id.id)]):
					if vals:
						for line in vals.questions_line_ids:
							create_rec = self.env['product.checklist'].create({'name': line.name, 'header_id': self.id})
			return super(MrpProductionInherit, self).action_confirm()

	@api.depends('origin')
	def _compute_mrp_sale_line_mapping(self):
		for rec in self:
			for sale_ref in rec.env['sale.order'].sudo().search([('name', '=', rec.origin)], limit=1):
				if sale_ref:
					for sale_line in sale_ref.env['sale.order.line'].sudo().search([('order_id', '=', sale_ref.id), ('product_template_id', '=', rec.bom_id.product_tmpl_id.id)], limit=1):
						if sale_line:
							rec.price_subtotal = sale_line.dp_unit_final_value
						else:
							rec.price_subtotal = 0.0
				else:
					rec.price_subtotal = 0.0

	price_subtotal = fields.Float(string='DP Value', compute="_compute_mrp_sale_line_mapping")



	@api.depends('state')
	def _compute_progress_hours(self):
		for mrp_status in self:
			if (mrp_status.state == 'draft'):
				mrp_status.progress = 0.00
			elif (mrp_status.state == 'confirmed'):
				mrp_status.progress = 8.00
			elif (mrp_status.state == 'design_stage'):
				mrp_status.progress = 16.00
			elif (mrp_status.state == 'ready_for_punching'):
				mrp_status.progress = 25
			elif (mrp_status.state == 'punching_done'):
				mrp_status.progress = 33.00
			elif (mrp_status.state == 'bending_done'):
				mrp_status.progress = 41.00
			elif (mrp_status.state == 'sub_assembly'):
				mrp_status.progress = 49.00
			elif (mrp_status.state == 'coloring_set'):
				mrp_status.progress = 58.00
			elif (mrp_status.state == 'coloring_sent'):
				mrp_status.progress = 66.00
			elif (mrp_status.state == 'color_sent'):
				mrp_status.progress = 66.00
			elif (mrp_status.state == 'coloring_completed'):
				mrp_status.progress = 74.00
			elif (mrp_status.state == 'final_assembly'):
				mrp_status.progress = 83.00
			elif (mrp_status.state == 'quality_approved'):
				mrp_status.progress = 91.00
			elif (mrp_status.state == 'cancel'):
				mrp_status.progress = 0.00
			else:
				mrp_status.progress = 100

	def action_assign(self):
		for production in self:
			production.move_raw_ids._action_assign()
			production.workorder_ids._refresh_wo_lines()
			production.write({'availability': True})
		return True

	def state_design(self):
		if self.order_id:
			if self.order_id.finance_team_approval_status == "approved":
				self.write({'state': 'design_stage'})
				self.progress_mapping()
			else:
				raise Warning(_('Finance team not approved for Manufacturing'))
		else:
			self.write({'state': 'design_stage'})
			self.progress_mapping()
	# def state_design(self):
	# 	if self.finance_team == "not_approve":
	# 		raise Warning(_('Accounts Team not approved for Manufacturing'))
	# 	elif self.finance_head == "not_approve":
	# 		raise Warning(_('Accounts Head not approved for Manufacturing'))
	# 	else:
	# 		self.write({'state': 'design_stage'})

	def state_punching(self):
		self.write({'state': 'ready_for_punching'})
		self.progress_mapping()

	def state_punching_done(self):
		self.write({'state': 'punching_done'})
		self.progress_mapping()

	def state_bending_done(self):
		self.write({'state': 'bending_done'})
		self.progress_mapping()

	def state_sub_assembly(self):
		self.write({'state': 'sub_assembly'})
		self.progress_mapping()

	def state_color_set(self):
		self.write({'state': 'coloring_set'})
		self.progress_mapping()

	def state_color_sent(self):
		self.write({'state': 'color_sent'})
		self.progress_mapping()

	def state_color_completed(self):
		self.write({'state': 'coloring_completed'})
		self.progress_mapping()

	def state_final_assembly(self):
		self.write({'state': 'final_assembly'})
		self.progress_mapping()

	def state_qua_approved(self):
		self.write({'state': 'quality_approved'})
		self.progress_mapping()

	def state_fg_credited(self):
		self.write({'state': 'fg_credited',
					'fg_credited_date': fields.Date.today()})
		self.progress_mapping()

	def state_desp(self):
		if self.finance_team_desp == "not_approve":
			raise Warning(_('Finance team not approved for Despatch'))
		else:
			self.write({'state': 'desp'})
			self.progress_mapping()

	def state_install(self):
		self.write({'state': 'installation'})
		self.progress_mapping()

	def open_produce_product(self):
		self.ensure_one()
		if self.bom_id.type == 'phantom':
			raise UserError(_('You cannot produce a MO with a bom kit product.'))
		if self.install_completed_dealer == "not_approve":
			raise UserError(_('Dealer is not Approved.'))
		if self.install_completed_customer == "not_approve":
			raise UserError(_('Customer is not Approved.'))
		action = self.env.ref('mrp.act_mrp_product_produce').read()[0]
		return action

	# def state_install_completed(self):
	#     self.write({'state': 'installtion_completed'})

	# def state_warranty_card(self):
	#     self.write({'state': 'warranty_card'})



			# 		if sale_ref:
			# 			mrp_origin.order_id = sale_ref.id
			# 		else:
			# 			mrp_origin.order_id = False
			# else:
			# 	mrp_origin.order_id = False

	is_visible = fields.Selection([('yes', 'Yes'),('no', 'No')], string='Visible')
	custom_progress = fields.Float("Custom Progress", help="Display progress of current task.",default=8.00, group_operator=False)
	serial_no = fields.Integer('Seria No', default=1)


	def progress_mapping(self):
		sum_progress = total_mrp = 0
		for sale_ref in self:
			for mrp_ref in sale_ref.env['mrp.production'].sudo().search([('origin', '=', sale_ref.origin)]):
				if mrp_ref and mrp_ref.state != 'cancel':
					total_mrp += len(mrp_ref)
					sum_progress += (mrp_ref.progress or 0.0)
					overall_progress_value = (sum_progress/total_mrp)
			for mrp_ref_all in mrp_ref.env['mrp.production'].sudo().search([('origin', '=', mrp_ref.origin)]):
				mrp_ref_all.update({
					'custom_progress': overall_progress_value})

	# @api.model
	# def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
	# 	res = super(MrpProductionInherit, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
	# 											 orderby=orderby, lazy=lazy)
	# 	if 'dealer_id' in fields:
	# 		for line in res:
	# 			print ("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
	# 			if '__domain' in line:
	# 				lines = self.search(line['__domain'])
	# 				a = "Customer Name"
	# 				for record in lines:
	# 					a = record.dealer_id
	# 				line['dealer_id'] = a
	# 	return res
				# if self.progress < mrp_ref.progress:
				# 	print (self.progress, "22222222222222", mrp_ref.progress)
				# 	self.write({'custom_progress': mrp_ref.progress})
				# elif self.progress > mrp_ref.progress:
				# 	print ("33333333333",self.progress)
				# 	self.write({'custom_progress': self.progress})
				# else:
				# 	self.write({'custom_progress': 0})

	# line_no = fields.Integer(string='Serial Number', readonly=False,False related=)


# <field name="activity_state"/>
#                     <progressbar field="activity_state" colors='{"planned": "success", "today": "warning", "overdue": "danger"}'/>

# widget="progressbar"/>
# < progressbar
# field = "activity_state"
# colors = '{"planned": "success", "today": "warning", "overdue": "danger"}'
# sum_field = "planned_revenue"
# help = "This bar allows to filter the opportunities based on scheduled activities." / >

class ProductChecklist(models.Model):
	_name = 'product.checklist'
	_description = "Product Checklist"

	name = fields.Char(string="Points to check",readonly=True)
	applicable = fields.Selection([('yes', 'Yes'),('no', 'No')], string='Applicable')
	remarks = fields.Char(string="Remarks")
	header_id = fields.Many2one('mrp.production')


class MrpProductionCron(models.Model):
	_name = 'mrp.production.cron'

	def mrp_production_visible(self):
		for sale_ref in self.env['sale.order'].sudo().search([]):
			for mrp_ref in sale_ref.env['mrp.production'].sudo().search([('origin', '=', sale_ref.name)], order='id ASC', limit=1):
				if not mrp_ref.is_visible:
					mrp_ref.write({'is_visible': 'no'})
				else:
					mrp_ref.write({'is_visible': 'yes'})

	# def mrp_sale_line_mapping(self):
	# 	for sale_ref in self.env['sale.order'].sudo().search([]):
	# 		for sale_line in sale_ref.order_line:
	# 			for mrp_ref in self.env['mrp.production'].sudo().search([('origin', '=', sale_ref.name), ('bom_id.product_tmpl_id', '=', sale_line.product_template_id.id)]):
	# 				if mrp_ref:
	# 					mrp_ref.write({'price_subtotal': 7})
	# 				else:
	# 					mrp_ref.write({'price_subtotal': 0.0})
