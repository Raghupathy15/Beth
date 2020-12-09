# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.osv import expression




class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    # def testing_log(self):
    #     lines = self
    #     for line in lines:
    #         for sale_line in line.order_line:
    #             if sale_line.tax_id:
    #                 msg = _("tax added line with %s ") % (sale_line.tax_id.name,)
    #                 line.message_post(body=msg)
    #     return lines

    # def create(self, vals):
    #     res = super(SaleOrderInherit, self).create(vals)
    #     for line in self:
    #         for sale_line in line.order_line:
    #             if sale_line.tax_id:
    #                 for tax in sale_line.tax_id:
    #                     msg = _("tax added line with %s ") % (tax.name,)
    #                     line.message_post(body=msg)
    #     return res
    #
    # def write(self, vals):
    #     res = super(SaleOrderInherit, self).write(vals)
    #     for line in self:
    #         for sale_line in line.order_line:
    #             if sale_line.tax_id:
    #                 for tax in sale_line.tax_id:
    #                     msg = _("tax added line with %s ") % (tax.name,)
    #                     line.message_post(body=msg)
    #     return res

    # partner_id = fields.Many2one(
    #     'res.partner', string='Customer',
    #     required=True, change_default=True, index=True, tracking=1,
    #     domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    type_of_order = fields.Selection([('express', 'Express'), ('standard', 'Standard'), ('lightning', 'Lightning'), ('token', 'Token')], string="Type Of Order", related='opportunity_id.type_of_order')
    scheme = fields.Many2one('scheme.master', string="Scheme", related='opportunity_id.scheme')
    dealer_id = fields.Many2one('res.partner', string="Dealer", store=True, related='opportunity_id.dealer_id')
    status_of_downpayment = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes')
    ], string='Down Payment', readonly=True, copy=False, index=True, tracking=3, default='yes')
    file = fields.Binary('POST SAP Quote BLPL', help="Upload File")
    file_name = fields.Char('File Name')

    sap_number = fields.Char('SAP Sale Quotation No')
    # sap_file = fields.Binary('SAP Sale Quotation File', help="Upload File")
    # sap_file_name = fields.Char('File Name')
    # dealer_price = fields.Integer('Dealer Price')
    # rrp = fields.Integer('RRP value')
    cancel_reason = fields.Char('Reason for Disapprove', tracking=True, copy=False)
    finance_team_approval_status = fields.Selection([('approved', 'Approved'), ('not_approved', 'Not Approve')],
                                             string="from payment", default='not_approved')
    sap_sale_no = fields.Char('SAP Sale Order Number from payment')
    sap_file = fields.Binary('SAP Sale Order File from payment', help="Upload File")
    sap_file_name = fields.Char('File Name from payment')

    state = fields.Selection([
        ('draft', '6A-Sale order requesting'),
        ('sale_request', '6B-Sale order requested'),
        ('sent', 'Quotation Sent'),
        ('approve', '7A-Sales quote for approval'),
        ('sale', '7B-Sale quote approved '),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    national_head_id = fields.Many2one("res.users", string="National Head", related="opportunity_id.national_head_id")
    regional_bdm_id = fields.Many2one("res.users", string="RM Direct", related="opportunity_id.regional_bdm_id")
    bdm_id = fields.Many2one("res.users", string="BDM Direct", related="opportunity_id.bdm_id")
    blpl_service_manager_id = fields.Many2one("res.users", string='BLPL Service Manager', related="opportunity_id.blpl_service_manager_id")
    blpl_service_engineer_id = fields.Many2one("res.users", string='Service Engineer', related="opportunity_id.blpl_service_engineer_id")
    blpl_master_id = fields.Many2one("blpl.master", string="Bethliving Store Profile", related="opportunity_id.blpl_master_id", store=True)
    blpl_store_team_id = fields.Many2one("res.users", string="BLPL Store Team", related="opportunity_id.blpl_store_team_id")
    interior_consultant_id = fields.Many2one("res.users", string="Interior Consoultants", related="opportunity_id.interior_consultant_id")
    sales_team_lead_id = fields.Many2one("res.users", string="Sales Team Lead", related="opportunity_id.sales_team_lead_id")
    sales_lead_id = fields.Many2one("res.users", string="Sales Lead", related="opportunity_id.sales_lead_id")
    blpl_service_techinician_id = fields.Many2one("res.users", string="Service Techinician", related="opportunity_id.blpl_service_techinician_id")

    deal_associate_id = fields.Many2one("res.users", string="Dealer", related="opportunity_id.deal_associate_id")
    blpl_associate_id = fields.Many2one("res.users", string="Associates", related="opportunity_id.blpl_associate_id")

#Franchisee
    franchisee_national_head_id = fields.Many2one("res.users", string="National Head", related="opportunity_id.franchisee_national_head_id")
    franchisee_rm_id = fields.Many2one('res.users', string='RM', related="opportunity_id.franchisee_rm_id")
    franchisee_bdm_id = fields.Many2one('res.users', string='BDM', related="opportunity_id.franchisee_bdm_id")
    franchisee_blpl_service_manager_id = fields.Many2one(comodel_name="res.users", string="BLPL Service Manager", related="opportunity_id.franchisee_blpl_service_manager_id")
    franchisee_blpl_service_engineer_id = fields.Many2one(comodel_name="res.users", string="Service Engineer", related="opportunity_id.franchisee_blpl_service_engineer_id")

    franchisee_master_id = fields.Many2one("franchisee.master", string="Franchisee Profile", related="opportunity_id.franchisee_master_id")
    franchisee_owner_id = fields.Many2one("res.users", string="Franchisee Owner", related="opportunity_id.franchisee_owner_id")

    sales_cordinators_id = fields.Many2one('res.users', string='Sales Cordinator', related="opportunity_id.sales_cordinators_id")

    sales_managere_id = fields.Many2one(comodel_name="res.users",
                                        string="Sales Manager", related="opportunity_id.sales_managere_id")
    sales_executive_id = fields.Many2one(comodel_name="res.users",
                                         string="Sales Executive", related="opportunity_id.sales_executive_id")
    service_technician_id = fields.Many2one(comodel_name="res.users",
                                            string="Service Techinician", related="opportunity_id.service_technician_id")
    franchisee_dealer_id = fields.Many2one(comodel_name="res.users", string="Dealer", related="opportunity_id.franchisee_dealer_id")
    associates_id = fields.Many2one(comodel_name="res.users",
                                    string="Associates", related="opportunity_id.associates_id")
    is_admin = fields.Boolean("Is Admin", compute="_compute_is_admin")

    @api.depends('user_id')
    def _compute_is_admin(self):
        admin_group = self.env.user.has_group('base.group_system')
        if admin_group:
            self.is_admin = True
        else:
            self.is_admin = False



    @api.depends('order_line.price_total')
    def _sum_amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_total_dp = amount_total_rrp = amount_total_discount = amount_total_forecast_discount = total_line_items = 0.0
            for line in order.order_line:
                amount_total_dp += line.price_subtotal
                amount_total_rrp += line.rrp_amount
                total_line_items += line.line_no
                if line.price_subtotal != 0.0:
                    amount_total_discount += ((line.price_unit * line.product_uom_qty) - line.price_subtotal)
                # amount_total_forecast_discount += line.discount



            order.update({
                'sum_total_dp': amount_total_dp,
                'sum_total_rrp': amount_total_rrp,
                'sum_total_discount': amount_total_discount,
                'sum_total_line_items': total_line_items,
                # 'sum_total_forecast_discount': amount_total_forecast_discount,
            })


    sum_total_dp = fields.Monetary(string='Total DP', store=True, readonly=True, compute='_sum_amount_all', tracking=True)
    sum_total_rrp = fields.Monetary(string='Total RRP', store=True, readonly=True, compute='_sum_amount_all', tracking=True)
    sum_total_discount = fields.Monetary(string='Total Discount', store=True, readonly=True, compute='_sum_amount_all', tracking=True)
    # sum_total_forecast_discount = fields.Monetary(string='Total Forecast Discount', store=True, readonly=True, compute='_sum_amount_all', tracking=True)
    sum_total_line_items = fields.Integer(string='Total Line Items', compute='_sum_amount_all')


    def state_sale_request(self):
        if self.sum_total_line_items == 0.0:
            raise UserError(_('Please add atleast one lineitem'))
        self.write({'state': 'sale_request'})
        crm_source_rec = self.env['crm.lead'].search(
            [('id', '=', self.opportunity_id.id)], limit=1)
        if crm_source_rec:
            crm_source_rec.write({'state': '6b_sale_requested'})


    def state_sale(self):
        # if self.dealer_price <= 0.00:
        #     raise UserError(_('The value of the dealer price must be positive.'))
        if self.file == False:
            raise UserError(_('Please Upload Quote File from BLPL SAP.'))
        # elif self.sap_file == False:
        #     raise UserError(_('Please Upload Quote File of SAP Sale Quotation.'))
        elif self.sap_number == False:
            raise UserError(_('Please Upload Quote File of SAP Sale Quotation No.'))
        else:
            self.write({'state': 'approve'})
            crm_source_rec = self.env['crm.lead'].search(
                [('id', '=', self.opportunity_id.id)], limit=1)
            if crm_source_rec:
                crm_source_rec.write({'state': '7_sale_order_created'})

    def action_cancel(self):
        if not self.cancel_reason:
            raise UserError(_('Please fill Disapprove Reason'))
        crm_source_rec = self.env['crm.lead'].search(
            [('id', '=', self.opportunity_id.id)], limit=1)
        if crm_source_rec:
            crm_source_rec.write({'state': '6_sale_order_requested'})
        return self.write({'state': 'cancel'})


    def action_confirm(self):
        super(SaleOrderInherit, self).action_confirm()
        crm_source_rec = self.env['crm.lead'].search(
            [('id', '=', self.opportunity_id.id)], limit=1)
        if crm_source_rec:
            crm_source_rec.write({'state': '7_approved_sale_order'})

    def action_draft(self):
        super(SaleOrderInherit, self).action_draft()
        if self.cancel_reason:
            self.cancel_reason = False
            self.file = False
            self.file_name = False
            # self.sap_file = False
            # self.sap_file_name = False
            self.sap_number = False


    # @api.onchange('self')
    # # def _onchange_discount(self):
    # @api.constrains("self")
    # @api.depends('name')
    # def compute_check_rule_date_from(self):
    # def check_rule_date_from(self):
    #     scheme_master = self.env['scheme.master'].search([])
    #     print(scheme_master, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     for scheme_rec in scheme_master:
    #         print("eeeeeeeeeeeeeeeeeeee", scheme_rec.to_date, scheme_rec.from_date, self.date_order,
    #               "wwwwwwwwwwwwwwwwww")
    #     scheme_validity = (
    #                 scheme_rec.from_date <= self.date_order and scheme_rec.to_date >= self.date_order)
    #     if scheme_validity:
    #         scheme_master.write({'scheme_active': True})
    #     else:
    #         scheme_master.write({'scheme_active': False})
    #     print(scheme_validity, "@@@@@@@@@@@@@@@@@@@@@@@")


class SaleAdvancePaymentInvExtend(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # advance_payment_method = fields.Selection([
    #     ('delivered', 'Regular invoice'),
    #     ('percentage', 'Down payment (percentage)'),
    #     ('fixed', 'Down payment (fixed amount)')
    # ], string='Create Invoice', default='percentage', required=True,
    #     help="A standard invoice is issued with all the order lines ready for invoicing, \
    #         according to their invoicing policy (based on ordered or delivered quantity).")

    amount = fields.Float('Payment', digits='Account',
                          help="The percentage of amount to be invoiced in advance, taxes excluded.")

    @api.onchange('advance_payment_method')
    def onchange_advance_payment_method(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if (sale_orders.type_of_order == 'express' or sale_orders.type_of_order == 'lightning'):
            self.advance_payment_method = 'percentage'
            return {'value': {'amount': 100}}
        elif (sale_orders.type_of_order == 'standard'):
            self.advance_payment_method = 'percentage'
            return {'value': {'amount': 50}}
        elif sale_orders.type_of_order == 'token':
            self.advance_payment_method = 'fixed'
        return {}

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders.status_of_downpayment == "yes":
            if (sale_orders.type_of_order == 'express' or sale_orders.type_of_order == 'lightning') and (self.advance_payment_method == 'percentage' and self.amount != 100.00):
                raise Warning(_('Order type is Express/Lightning so please make" (100% Payment)'))
            elif (sale_orders.type_of_order == 'standard') and (self.advance_payment_method == 'percentage' and self.amount != 50.00):
                raise Warning(_('Order type is Standard so please make" (50% Payment'))
            # elif self.advance_payment_method == 'percentage' and sale_orders.type_of_order == 'standard':
            #     raise Warning(_('Order type is Standard so please make" (50% Payment'))
            # elif (self.advance_payment_method == 'percentage' and self.amount != 50.00) or (
            #         self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00) and sale_orders.type_of_order == 'standard':
            #     raise Warning(_('Order type is Standard so please make" (50% Payment)'))
            elif (self.advance_payment_method == 'percentage' and self.amount <= 0.00) or (
                    self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00) and sale_orders.type_of_order == 'token':
                raise Warning(_('Value should be positive'))
            else:
                sale_orders.write({'status_of_downpayment': "no"})

        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
                else:
                    tax_ids = taxes.ids
                context = {'lang': order.partner_id.lang}
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                del context
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}



class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    # @api.depends('sequence', 'order_id')
    # def _compute_get_number(self):
    #     number = 1
    #     for line in self:
    #         line.line_no = number
    #         number += 1


    line_no = fields.Integer(string='Serial Number', readonly=False, default=1)

    # line_status = fields.Selection([
    #     ('new_entry', '01-New Entry'),
    #     ('design_stage', '02-Design Stage'),
    #     ('punch', '03-Ready For Punching'),
    #     ('punch_done', '04-Punching Done'),
    #     ('bending_done', '05-Bending Done'),
    #     ('sub_assembly', '06-Sub-Assembly'),
    #     ('coloring_to_be_sent', '07-Coloring To be Sent'),
    #     ('coloring_sent', '08-Coloring Sent'),
    #     ('coloring_completed', '09-Coloring Completed'),
    #     ('final_assembly', '10-Final Assembly'),
    #     ('quality_approved', '11-Quality Approved'),
    #     ('fg_credited', '12-FG Creited'),
    # ], string='Status', copy=False, index=True, tracking=3, default="new_entry")

    date_order = fields.Datetime(string="Order Date", related='order_id.date_order')
    dealer_id = fields.Many2one('res.partner', string="Customer", related='order_id.dealer_id')
    partner_id = fields.Many2one('res.partner', string="Customer", related='order_id.partner_id')
    product_code = fields.Integer('SAP Code', related="product_template_id.product_code")



    # scheme_id = fields.Many2one('scheme.master', string="Discount %")

    # scheme_id = fields.Many2one('scheme.master', string="Discount %", domain="[('from_date', '<=', context_today().strftime('%%Y-%%m-%%d')), ('to_date', '>=', context_today().strftime('%%Y-%%m-%%d'))]")
    scheme_id = fields.Many2one('scheme.master', string="Disc %", domain="[('from_date', '<=', date_order), ('to_date', '>=', date_order), ('partner_ids', '=', partner_id)]")
    scheme_discount = fields.Float('Scheme Discount',related='scheme_id.discount')



    # responsible_id = fields.Many2one('res.users', string="Responsible", domain=lambda self: [
    #     ('groups_id', 'in', self.env.ref('lunch.group_lunch_manager').id)],
    #                                  default=lambda self: self.env.user,
    #                                  help="The responsible is the person that will order lunch for everyone. It will be used as the 'from' when sending the automatic email.")
    #

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'scheme_id', 'scheme_discount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            sum_dp_value_after_discount = line.price_unit * (1 - (line.scheme_discount or 0.0) / 100.0)
            sum_dp_unit_final_value = sum_dp_value_after_discount * (1 - (line.discount or 0.0) / 100.0)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] * (1 - (line.scheme_discount or 0.0) / 100.0),
                'rrp_amount': (line.rrp_unit_price * line.product_uom_qty),
                'dp_value_after_discount': (sum_dp_value_after_discount),
                'dp_unit_final_value': (sum_dp_unit_final_value),
                'test': (sum_dp_unit_final_value * line.product_uom_qty)
            })

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'scheme_id')
    # def _compute_amount_extend(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         sum_dp_value_after_discount = line.price_unit * (1 - (line.scheme_discount or 0.0) / 100.0)
    #         sum_dp_unit_final_value = sum_dp_value_after_discount * (1 - (line.discount or 0.0) / 100.0)
    #         line.update({
    #             'rrp_amount': (line.rrp_unit_price * line.product_uom_qty),
    #             'dp_value_after_discount': (sum_dp_value_after_discount),
    #             'dp_unit_final_value': (sum_dp_unit_final_value),
    #             'test': (sum_dp_unit_final_value * line.product_uom_qty)
    #         })

    dp_value_after_discount = fields.Float(compute='_compute_amount', string='DP Amt', readonly=True, store=True)
    rrp_unit_price = fields.Float('RRP', related='product_id.rrp_unit_price')
    rrp_amount = fields.Float(compute='_compute_amount', string='RRP Amt', readonly=True, store=True)

    dp_unit_final_value = fields.Float(compute='_compute_amount', string='DP Final Value', readonly=True, store=True)
    test = fields.Float(compute='_compute_amount', string='Test Subtotal', readonly=True, store=True)


    class SaleProductConfigurator(models.TransientModel):
        _inherit = 'sale.product.configurator'
        _description = 'Sale Product Configurator'

        sale_description = fields.Text("Description", related="product_template_id.description_sale")