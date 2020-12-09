# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
# import time
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    # _rec_name = "partner_id"
    def name_get(self):
        result = []
        for a in self:
            name = a.partner_id.name
            result.append((a.id, name))
        return result

    type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Payments'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
        default="entry", change_default=True)

    @api.depends('invoice_origin')
    def _compute_sale_source(self):
        is_admin_group = self.env.user.has_group('base.group_system')
        is_finance_acc_manager = self.env.user.has_group('ind_access_extend.group_finance_account_manager_admin')
        is_finance_executive = self.env.user.has_group('ind_access_extend.group_finance_executive_admin')
        is_finance_head = self.env.user.has_group('ind_access_extend.group_finance_head_admin')
        if is_admin_group:
            self.is_admin_group = True
        else:
            self.is_admin_group = False
        if is_finance_acc_manager or is_finance_executive or is_finance_head:
            self.is_finance_group = True
        else:
            self.is_finance_group = False
        if self.invoice_origin:
            orders = self.env['sale.order'].search(
                [('name', '=', self.invoice_origin)], limit=1)
            if orders:
                self.sale_source_id = orders.id
            else:
                self.sale_source_id = False
        else:
            self.sale_source_id = False


    is_admin_group = fields.Boolean("Is Admin", compute="_compute_sale_source")
    is_finance_group = fields.Boolean("Is Finance", compute="_compute_sale_source")
    sap_sale_no = fields.Char('SAP Sale Order Number')
    sap_file = fields.Binary('SAP Sale Order File', help="Upload File")
    sap_file_name = fields.Char('File Name')
    finance_team_approval = fields.Selection([('approved', 'Approved'), ('not_approved', 'Not Approve')], string="Finance Team Approval for MRP", default='not_approved')
    finance_conf_details = fields.Text("Confirmation Details", help="Confirmation Details")
    approved_id = fields.Many2one(comodel_name="res.users", string="MRP Approved by")
    sale_source_id = fields.Many2one("sale.order", string="Sale Source", compute="_compute_sale_source")
    dealer_id = fields.Many2one("res.partner", string='Customer', related="sale_source_id.dealer_id")
    national_head_id = fields.Many2one("res.users", string="National Head", related="sale_source_id.national_head_id")
    regional_bdm_id = fields.Many2one("res.users", string="RM Direct", related="sale_source_id.regional_bdm_id")
    bdm_id = fields.Many2one("res.users", string="BDM Direct", related="sale_source_id.bdm_id")
    blpl_service_manager_id = fields.Many2one("res.users", string='BLPL Service Manager',
                                              related="sale_source_id.blpl_service_manager_id")
    blpl_service_engineer_id = fields.Many2one("res.users", string='Service Engineer',
                                               related="sale_source_id.blpl_service_engineer_id")
    blpl_master_id = fields.Many2one("blpl.master", string="Bethliving Store Profile",
                                     related="sale_source_id.blpl_master_id")
    blpl_store_team_id = fields.Many2one("res.users", string="BLPL Store Team",
                                         related="sale_source_id.blpl_store_team_id")
    interior_consultant_id = fields.Many2one("res.users", string="Interior Consoultants",
                                             related="sale_source_id.interior_consultant_id")
    sales_team_lead_id = fields.Many2one("res.users", string="Sales Team Lead",
                                         related="sale_source_id.sales_team_lead_id")
    sales_lead_id = fields.Many2one("res.users", string="Sales Lead", related="sale_source_id.sales_lead_id")
    blpl_service_techinician_id = fields.Many2one("res.users", string="Service Techinician",
                                                  related="sale_source_id.blpl_service_techinician_id")

    deal_associate_id = fields.Many2one("res.users", string="Dealer", related="sale_source_id.deal_associate_id")
    blpl_associate_id = fields.Many2one("res.users", string="Associates", related="sale_source_id.blpl_associate_id")

    # Franchisee
    franchisee_national_head_id = fields.Many2one("res.users", string="National Head",
                                                  related="sale_source_id.franchisee_national_head_id")
    franchisee_rm_id = fields.Many2one('res.users', string='RM', related="sale_source_id.franchisee_rm_id")
    franchisee_bdm_id = fields.Many2one('res.users', string='BDM', related="sale_source_id.franchisee_bdm_id")
    franchisee_blpl_service_manager_id = fields.Many2one(comodel_name="res.users", string="BLPL Service Manager",
                                                         related="sale_source_id.franchisee_blpl_service_manager_id")
    franchisee_blpl_service_engineer_id = fields.Many2one(comodel_name="res.users", string="Service Engineer",
                                                          related="sale_source_id.franchisee_blpl_service_engineer_id")

    franchisee_master_id = fields.Many2one("franchisee.master", string="Franchisee Profile",
                                           related="sale_source_id.franchisee_master_id")
    franchisee_owner_id = fields.Many2one("res.users", string="Franchisee Owner",
                                          related="sale_source_id.franchisee_owner_id")

    sales_cordinators_id = fields.Many2one('res.users', string='Sales Cordinator',
                                           related="sale_source_id.sales_cordinators_id")

    sales_managere_id = fields.Many2one(comodel_name="res.users",
                                        string="Sales Manager", related="sale_source_id.sales_managere_id")
    sales_executive_id = fields.Many2one(comodel_name="res.users",
                                         string="Sales Executive", related="sale_source_id.sales_executive_id")
    service_technician_id = fields.Many2one(comodel_name="res.users",
                                            string="Service Techinician",
                                            related="sale_source_id.service_technician_id")
    franchisee_dealer_id = fields.Many2one(comodel_name="res.users", string="Dealer",
                                           related="sale_source_id.franchisee_dealer_id")
    associates_id = fields.Many2one(comodel_name="res.users",
                                    string="Associates", related="sale_source_id.associates_id")


    queue_mrp = fields.Char("Queued for manufacturing")


    def get_mrp(self):
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manufacture',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            # 'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False, 'edit': True}"
        }

    def state_full_payment_approve_mrp(self):
        is_finance_acc_manager = self.env.user.has_group('ind_access_extend.group_finance_account_manager_admin')
        is_finance_executive = self.env.user.has_group('ind_access_extend.group_finance_executive_admin')
        is_finance_head = self.env.user.has_group('ind_access_extend.group_finance_head_admin')
        sale_orders_rec = self.env['sale.order'].sudo().search(
            [('name', '=', self.invoice_origin)], limit=1)
        if self.sap_sale_no and self.sap_file:
            if self.finance_conf_details:
                if self.amount_residual == 0.0 and sale_orders_rec and (is_finance_acc_manager or is_finance_executive):
                    self.write({'finance_team_approval': 'approved',
                                'approved_id': self.env.uid})
                    sale_orders_rec.sudo().write({'finance_team_approval_status': 'approved',
                                           'sap_sale_no': self.sap_sale_no,
                                           'sap_file': self.sap_file,
                                           'sap_file_name': self.sap_file_name})
                elif self.amount_residual != 0.0 and sale_orders_rec and is_finance_head:
                    self.write({'finance_team_approval': 'approved',
                                'approved_id': self.env.uid})
                    sale_orders_rec.sudo().write({'finance_team_approval_status': 'approved',
                                           'sap_sale_no': self.sap_sale_no,
                                           'sap_file': self.sap_file,
                                           'sap_file_name': self.sap_file_name})
                else:
                    # self.write({'finance_team_approval': 'not_approved'})
                    # sale_orders_rec.write({'finance_team_approval_status': 'not_approved'})
                    raise UserError(_('You are not an authorized person to approve'))
            else:
                raise UserError(_('Before Approve Please Enter Confirmation Details'))
        else:
            raise UserError(_('Please update SAP Sale Order Numbe / File'))




