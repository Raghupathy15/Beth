# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import re



class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"
    _rec_name = "dealer_id"

    def name_get(self):
        result = []
        for a in self:
            name = a.dealer_id.name
            result.append((a.id, name))
        return result

    # def _group_associated_domain(self):
    #     group = self.env.ref('ind_access_extend.group_blpl_associates_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    # def _group_associated_domain(self):
    #     company_id = self.env.company
    #     if company_id.company_branch_type == 'direct_store':
    #         group = self.env.ref('ind_access_extend.group_blpl_associates_admin', raise_if_not_found=False)
    #         # group = ['|', ('company_id', '=', False), ('company_id', '=', company_id.id)]
    #     elif company_id.company_branch_type == 'franchisee':
    #         group = self.env.ref('ind_access_extend.group_associates_admin', raise_if_not_found=False)
    #     else:
    #         a = 1
    #     return [('groups_id', 'in', group.ids)] if group else []

    # def compute_current_login_groups(self):
    #     print ("1111111111111111111111111111")
    #     is_group_national_head_admin= self.env.user.has_group('ind_crm_extend.group_national_head_admin')
    #     is_blpl_group_regional_bdm_admin = self.env.user.has_group('ind_crm_extend.group_regional_bdm_admin')
    #     is_blpl_group_bdm_admin = self.env.user.has_group('ind_crm_extend.group_bdm_admin')
    #     is_blpl_group_blpl_service_manager_admin = self.env.user.has_group('ind_crm_extend.group_blpl_service_manager_admin')
    #     is_blpl_group_blpl_service_engineer_admin = self.env.user.has_group('ind_crm_extend.group_blpl_service_engineer_admin')
    #     is_blpl_group_blpl_store_team_admin = self.env.user.has_group('ind_crm_extend.group_blpl_store_team_admin')
    #     is_blpl_group_interior_consultant_admin = self.env.user.has_group('ind_crm_extend.group_interior_consultant_admin')
    #     is_blpl_group_sales_team_lead_admin = self.env.user.has_group('ind_crm_extend.group_sales_team_lead_admin')
    #     is_blpl_group_sales_lead_admin = self.env.user.has_group('ind_crm_extend.group_sales_lead_admin')
    #     is_blpl_group_blpl_service_tech_admin = self.env.user.has_group('ind_crm_extend.group_blpl_service_tech_admin')
    #     is_blpl_group_dealer_associates_admin = self.env.user.has_group('ind_crm_extend.group_dealer_associates_admin')
    #     is_blpl_group_blpl_associates_admin = self.env.user.has_group('ind_crm_extend.group_blpl_associates_admin')
    #
    #
    #     if is_blpl_group_regional_bdm_admin:
    #         print (is_blpl_group_regional_bdm_admin, "11111111111111111111111111")
    #         self.write({
    #             'current_user_group': 'National Head'})
    #     else:
    #         self.current_user_group = False


    # def _group_associated_domain(self):
    #     company_id = self.env.company
    #     print (self.company_id.name,company_id, "1111111111111111111111111")
    #     if company_id.company_branch_type == 'direct_store':
    #         group = self.env.ref('ind_access_extend.group_blpl_associates_admin', raise_if_not_found=False)
    #     else:
    #         group = self.env.ref('ind_access_extend.group_associates_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []

    name = fields.Many2one('opportunity.master', 'Opportunity', required=True, index=True, default=1)
    type_of_order = fields.Selection(
        [('express', 'Express'), ('standard', 'Standard'), ('lightning', 'Lightning'), ('token', 'Token')],
        string="Type Of Order")
    # customer_budget = fields.Char(string="Customer Budget")
    # customer_budget_value = fields.Integer(string="Customer Budget Value")
    visit_date = fields.Date(string="Show Room Visit Date", readonly=False, store=True)
    # is_visit = fields.Boolean(string="Is Show Room Visited", compute="_compute_visit", default=False)
    follow_date = fields.Date(string="Last FollowUp Date", default=datetime.now())
    next_follow_date = fields.Date(string="Next FollowUp Date")
    bounce_date = fields.Date(string="Bounce Date", readonly=False, store=True)
    dealer_id = fields.Many2one('res.partner', string="Customer", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    dealer_phone = fields.Char(string="Customer Phone", related="dealer_id.phone")
    dealer_email = fields.Char(string="Customer Email", related="dealer_id.email")
    source_dealer_id = fields.Many2one('res.users', string="Delaer")
    freelancer_id = fields.Many2one('res.users', string="Freelancer")


    # associate_id = fields.Many2one('res.users', string="Associate Name", domain=_group_associated_domain)
    associate_id = fields.Many2one('res.users', string="Associate Name")

    # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    # domain = "['|',('company_id', '=', company_id),('company_id', '=', False)]" / >
    # domain = lambda self: [('groups_id', 'in', self.env.ref('fleet.fleet_group_manager').id)])
    approximate_budget_id = fields.Many2one('budget.master', string="Approximate Budget")
    quote_value = fields.Char(string="Quote value(RRP Value)")

    order_value = fields.Integer(string="Order Value")
    order_date = fields.Date(string="Order Date", readonly=False, store=True)
    anticipate_date = fields.Date(string="Anticipated Delivery Date")
    scheme = fields.Many2one('scheme.master', string="Scheme")
    # scheme_file = fields.Binary(string="Scheme File", related='scheme.doc')
    # scheme_file_name = fields.Char(string="Scheme File Name", related='scheme.doc_name')
    # file = fields.Binary('File', help="Upload File")
    # file_name = fields.Char('File Name')

    # lost_reason_id = fields.Many2one('crm.lost.reason', string="Bounce Reason")
    customer_pan = fields.Char(string="Customer PAN", related="dealer_id.customer_pan")
    seq_name = fields.Char(string="Lead Id", required=True, copy=False, default='New', readonly=False)
    custom_create_date = fields.Datetime(string='Lead Created on', readonly=False, default=lambda self: fields.Datetime.now())

    fifth_state = fields.Boolean(string="5th state", default=False)
    fifth_5a_token_state = fields.Boolean(string="5A Token state", default=False)

    crm_admin_state_access = fields.Boolean('State Access', default=False, compute='compute_crm_admin')
    quote_date = fields.Date(string="Quote Date", readonly=False, store=True)
    lead_doc_line_ids = fields.One2many('crm.doc.line', 'crm_source_id', string='Files')
    is_quote_create = fields.Boolean(string='Quote Create or Not', compute='_compute_is_quote_create')
    email_from = fields.Char('Dealer Email', readonly=True, default=" ", help="Email address of the contact", tracking=40, index=True)
    phone = fields.Char('Dealer Phone', tracking=50)
    meeting = fields.Selection([('online_meet', 'Online Meeting'), ('skip_meet', 'Skip Meeting')], string="Meeting",tracking=True, default= False)
    meeting_date = fields.Date(string="Online Meeting Date", store=True, tracking=True)
    current_user_id = fields.Many2one('res.users',string='Lead Created by', default=lambda self: self.env.user, store=True,)
    current_user_email_address = fields.Char(string='User Email', related="current_user_id.login")

    # current_user_group = fields.Char("Designation", compute="compute_current_login_groups", store=False)
    # a_id = fields.Many2one('res.partner', related='current_user_id.partner_id')
    partner_id = fields.Many2one('res.partner', string='Customer',store=True, tracking=10, index=True, related='company_id.partner_id',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    house_warming_date = fields.Date(string="House Warming Date /Handing Over Date",tracking=True)
    sale_req_date = fields.Date(string="Sale Order Requesting Date", tracking=True)
    company_branch_type = fields.Selection([
        ('direct_store', 'Direct Store'),
        ('franchisee', 'Franchisee')], string='Company Type', related='company_id.company_branch_type')

    state = fields.Selection([
        ('draft', 'Creation of lead'),
        ('1_new_lead', '1-New lead'),
        ('2_first_contact', '2-First contact'),
        ('2a_online_meet_status', '2A-Online Meeting'),
        ('3_showroom_visit', '3-ShowRoom visit'),
        ('4_quote', '4-Quote'),
        ('5a_order_placed', '5A-Order placed token'),
        ('5b_order_placed', '5B-Order placed express'),
        ('5c_order_placed', '5C-Order placed standard'),
        ('5d_order_placed', '5D-Order placed lightning'),
        ('6_sale_order_requested', '6A-Sale order requesting'),
        ('6b_sale_requested', '6B-Sale order requested'),
        ('7_sale_order_created', '7A-Sales order for approval'),
        ('7_approved_sale_order', '7B-Sales order approved'),
        ('8_bounced', '8-Bounced'),
    ], string='State', copy=False, index=True, readonly=False,
        store=True, tracking=True, default='draft')


    @api.onchange('anticipate_date')
    def anticipate_date_cons(self):
        min_date = fields.Date.today()
        if self.anticipate_date and self.anticipate_date < min_date:
            raise ValidationError(_("Date is not valid, please select today or future date."))
        else:
            return False

    @api.onchange('follow_date')
    def follow_date_cons(self):
        min_date = fields.Date.today()
        if self.follow_date and self.follow_date < min_date:
            raise ValidationError(_("Date is not valid, Please select today or future date."))
        else:
            return False

    @api.onchange('next_follow_date')
    def next_followe_date_cons(self):
        min_date = fields.Date.today()
        if self.next_follow_date and self.next_follow_date < min_date:
            raise ValidationError(_("Date is not valid, Please select today or future date."))
        else:
            return False

    @api.onchange('house_warming_date')
    def house_warming_date_cons(self):
        min_date = fields.Date.today()
        if self.house_warming_date and self.house_warming_date < min_date:
            raise ValidationError(_("Date is not valid, Please select today or future date."))
        else:
            return False

    # def _group_regional_bdm_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_regional_bdm_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    # def _group_bdm_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_bdm_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    #
    # def _group_blpl_store_team_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_blpl_store_team_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    #
    # def _group_interior_consultant_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_interior_consultant_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    #
    # def _group_sales_team_lead_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_sales_team_lead_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    #
    # def _group_sales_lead_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_sales_lead_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []
    #
    # def _group_dealer_associates_user_domain(self):
    #     group = self.env.ref('ind_access_extend.group_dealer_associates_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []


# blpl Master
    regional_bdm_ids = fields.Many2many('res.users', string='RM Direct', related="blpl_master_id.regional_bdm_ids")
    bdm_ids = fields.Many2many('res.users', string='BDM Direct', related="blpl_master_id.bdm_ids")
    blpl_service_manager_ids = fields.Many2many('res.users', string='BLPL Service Manager', related="blpl_master_id.blpl_service_manager_ids")
    blpl_service_engineer_ids = fields.Many2many('res.users',
                                                 string='Service Engineer', related="blpl_master_id.blpl_service_engineer_ids")
    blpl_store_team_ids = fields.Many2many("res.users", string="Store Manager", related="blpl_master_id.blpl_store_team_ids")
    interior_consultant_ids = fields.Many2many("res.users",
                                               string="Interior Consoultant", related="blpl_master_id.interior_consultant_ids")
    sales_team_lead_ids = fields.Many2many("res.users", string="Sales Team Lead", related="blpl_master_id.sales_team_lead_ids")
    sales_lead_ids = fields.Many2many("res.users", string="Sales Lead", related="blpl_master_id.sales_lead_ids")

    blpl_service_techinician_ids = fields.Many2many("res.users", string="Service Techinician", related="blpl_master_id.blpl_service_techinician_ids")

    deal_associate_ids = fields.Many2many("res.users", string="Dealer", related="blpl_master_id.deal_associate_ids")
    blpl_associate_ids = fields.Many2many("res.users", string="Associates", related="blpl_master_id.blpl_associate_ids")

    national_head_id = fields.Many2one("res.users", string="National Head", related="blpl_master_id.national_head_id", tracking=True)
    regional_bdm_id = fields.Many2one("res.users", string="RM Direct", tracking=True,
                                       domain="[('id', 'in', regional_bdm_ids)]")
    bdm_id = fields.Many2one("res.users", string="BDM Direct",
                                       domain="[('id', 'in', bdm_ids)]")
    blpl_service_manager_id = fields.Many2one("res.users", string='BLPL Service Manager', tracking=True,
                                       domain="[('id', 'in', blpl_service_manager_ids)]")
    blpl_service_engineer_id = fields.Many2one("res.users", string='Service Engineer', tracking=True,
                                       domain="[('id', 'in', blpl_service_engineer_ids)]")
    blpl_master_id = fields.Many2one("blpl.master", string="Bethliving Store Profile", tracking=True)

    blpl_store_team_id = fields.Many2one("res.users", string="BLPL Store Team", tracking=True,
                                       domain="[('id', 'in', blpl_store_team_ids)]")
    interior_consultant_id = fields.Many2one("res.users", string="Interior Consoultants", tracking=True,
                                       domain="[('id', 'in', interior_consultant_ids)]")
    sales_team_lead_id = fields.Many2one("res.users", string="Sales Team Lead", tracking=True,
                                       domain="[('id', 'in', sales_team_lead_ids)]")
    sales_lead_id = fields.Many2one("res.users", string="Sales Lead", tracking=True,
                                       domain="[('id', 'in', sales_lead_ids)]")
    blpl_service_techinician_id = fields.Many2one("res.users", string="Service Techinician",
                                       domain="[('id', 'in', blpl_service_techinician_ids)]")

    deal_associate_id = fields.Many2one("res.users", string="Dealer", tracking=True,
                                       domain="[('id', 'in', deal_associate_ids)]")
    blpl_associate_id = fields.Many2one("res.users", string="Associates", tracking=True,
                                       domain="[('id', 'in', blpl_associate_ids)]")

    def _compute_is_blpl_team(self):
        if  (self.regional_bdm_id.id) or (self.bdm_id.id) or (self.blpl_store_team_id.id) or (self.interior_consultant_id.id) or (self.sales_team_lead_id.id) or (self.sales_lead_id.id) or (self.deal_associate_id.id) == self.env.uid:
            self.is_blpl_team = True
        else:
            self.is_blpl_team = False
        if self.national_head_id.id == self.env.uid:
            self.is_national_head = True
        else:
            self.is_national_head = False

    @api.onchange('meeting')
    def _onchange_meeting_date(self):
        if self.meeting == 'online_meet':
            self.meeting_date = fields.Date.today()
        else:
            self.meeting_date = False

    # def _compute_is_blpl_team(self):
    #     if self.blpl_master_id:
    #         self.is_blpl_team = True
    #     if self.franchisee_master_id:
    #         self.is_blpl_team = False
    #     # else:
    #     #     self.is_blpl_team = False
    #     if self.national_head_id.id == self.env.uid:
    #         self.is_national_head = True
    #     else:
    #         self.is_national_head = False





    # is_blpl_team = fields.Boolean(string="Is BLPL", compute="_compute_is_blpl_team")
    # is_national_head = fields.Boolean(string="Is National Head", compute="_compute_is_blpl_team")

#end blpl Master
#Franchisee Master
    franchisee_national_head_id = fields.Many2one("res.users", string="National Head", related="franchisee_master_id.franchisee_national_head_id")
    franchisee_rm_ids = fields.Many2many(comodel_name="res.users", string="RM", related="franchisee_master_id.franchisee_rm_ids")
    franchisee_bdm_ids = fields.Many2many(comodel_name="res.users",  string="BDM", related="franchisee_master_id.franchisee_bdm_ids")
    franchisee_blpl_service_manager_ids = fields.Many2many(comodel_name="res.users", string="BLPL Service Manager", related="franchisee_master_id.franchisee_blpl_service_manager_ids")
    franchisee_blpl_service_engineer_ids = fields.Many2many(comodel_name="res.users", string="Service Engineer", related="franchisee_master_id.franchisee_blpl_service_manager_ids")
    franchisee_owner_ids = fields.Many2many("res.users", string="Franchisee Owner", related="franchisee_master_id.franchisee_owner_ids")

    sales_cordinators_ids = fields.Many2many('res.users', string='Sales Cordinator', related="franchisee_master_id.sales_cordinators_ids")
    sales_managere_ids = fields.Many2many(comodel_name="res.users", string="Sales Manager", related="franchisee_master_id.sales_managere_ids")
    sales_executive_ids = fields.Many2many(comodel_name="res.users", string="Sales Executive", related="franchisee_master_id.sales_executive_ids")
    service_technician_ids = fields.Many2many(comodel_name="res.users", string="Service Techinician", related="franchisee_master_id.service_technician_ids")
    franchisee_dealer_ids = fields.Many2many(comodel_name="res.users", string="Dealer", related="franchisee_master_id.franchisee_dealer_ids")
    associates_ids = fields.Many2many(comodel_name="res.users", string="Associates", related="franchisee_master_id.associates_ids")


    #####
    franchisee_rm_id = fields.Many2one('res.users', string='RM', tracking=True,
                                       domain="[('id', 'in', franchisee_rm_ids)]")
    franchisee_bdm_id = fields.Many2one('res.users', string='BDM', tracking=True,
                                           domain="[('id', 'in', franchisee_bdm_ids)]")
    franchisee_blpl_service_manager_id = fields.Many2one(comodel_name="res.users", string="BLPL Service Manager",
                                                           tracking=True, domain="[('id', 'in', franchisee_blpl_service_manager_ids)]")
    franchisee_blpl_service_engineer_id = fields.Many2one(comodel_name="res.users", string="Service Engineer",
                                                            tracking=True, domain="[('id', 'in', franchisee_blpl_service_engineer_ids)]")

    franchisee_master_id = fields.Many2one("franchisee.master", string="Team Name", tracking=True)

    franchisee_profile_id = fields.Many2one('res.partner', string='Franchisee Profile', store=True,
                                            related='franchisee_master_id.franchisee_profile_id',
                                            domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    franchisee_owner_id = fields.Many2one("res.users", string="Franchisee Owner", tracking=True, domain="[('id', 'in', franchisee_owner_ids)]")


    sales_cordinators_id = fields.Many2one('res.users', string='Sales Cordinator', tracking=True, domain="[('id', 'in', sales_cordinators_ids)]")

    sales_managere_id = fields.Many2one(comodel_name="res.users",
                                          string="Sales Manager", tracking=True, domain="[('id', 'in', sales_managere_ids)]")
    sales_executive_id = fields.Many2one(comodel_name="res.users",
                                           string="Sales Executive", tracking=True, domain="[('id', 'in', sales_executive_ids)]")
    service_technician_id = fields.Many2one(comodel_name="res.users",
                                              string="Service Technician", tracking=True, domain="[('id', 'in', service_technician_ids)]")
    franchisee_dealer_id = fields.Many2one(comodel_name="res.users", string="Dealer", tracking=True, domain="[('id', 'in', franchisee_dealer_ids)]")
    associates_id = fields.Many2one(comodel_name="res.users",
                                      string="Associates", tracking=True, domain="[('id', 'in', associates_ids)]")

# End Franchisee Master

    def _compute_is_quote_create(self):
        orders = self.env['sale.order'].search(
            [('opportunity_id', '=', self.id)], limit=1)
        if orders and (
                self.state == '5b_order_placed' or self.state == '5c_order_placed'
                or self.state == '5d_order_placed'):
            self.is_quote_create = True
        elif (
                self.state == 'draft' or self.state == '1_new_lead' or self.state == '2_first_contact' or self.state == '3_showroom_visit' or self.state == '4_quote'):
            self.is_quote_create = False
        if not orders and (
                self.state == '5b_order_placed' or self.state == '5c_order_placed'
                or self.state == '5d_order_placed' or self.state == '6_sale_order_requested'):
            self.is_quote_create = True
        else:
            self.is_quote_create = False

    # @api.depends("visit_date")
    # def _compute_visit(self):
    #     if self.visit_date:
    #         self.is_visit = True
    #     else:
    #         self.is_visit = False

    # @api.depends("state")
    # def compute_state(self):
    #     # self.ensure_one()
    # if self.id:
    #     sale_rec = self.env['sale.order'].sudo().search([('opportunity_id', '=', self.id)], limit=1)
    #     print (sale_rec, "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    #     if sale_rec.state == 'draft':
    #         self.update({
    #             'state': '6_sale_order_requested',
    #         })
    #         # self.state = '6_sale_order_requested'
    #     elif sale_rec.state == 'approve':
    #         self.update({
    #             'state': '7_sale_order_created',
    #         })
    # self.state = '7_sale_order_created'

    @api.depends('user_id')
    def compute_crm_admin(self):
        var = self.env.user.has_group('ind_crm_extend.group_crm_admin')
        if var:
            self.crm_admin_state_access = True
        else:
            self.crm_admin_state_access = False

    @api.model
    def create(self, vals):
        if vals.get('seq_name', _('New')) == _('New'):
            vals['seq_name'] = self.env['ir.sequence'].next_by_code('crm.lead')
        return super(CrmLeadInherit, self).create(vals)


    def write(self, vals):
        # if self.follow_date:
        #     vals['next_follow_date'] = self.follow_date + timedelta(days=+7)
        if 'stage_id' in vals:
            stage_id = self.env['crm.stage'].browse(vals['stage_id'])
            if stage_id.is_showroom_visit:
                vals.update({'visit_date': fields.Date.today()})
            # if stage_id.is_quote:
            #     self.action_sale_quotations_new()
            #     self.self.action_new_quotation()

        return super(CrmLeadInherit, self).write(vals)

    @api.onchange('follow_date')
    def onchange_followup(self):
        self.next_follow_date = self.follow_date + timedelta(days=+7)

    def action_crm_lead(self):
        self.ensure_one()
        return {
            'name': _('Lead or Opportunity'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'crm.lead',
            'domain': [('type', '=', self.type)],
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {'default_type': self.type}
        }

    def state_lead(self):
        self.write({'state': '1_new_lead',
                    'follow_date': fields.Date.today(),
                    'fifth_state': False})

    def state_first_contact(self):
        self.write({'state': '2_first_contact',
                    'follow_date': fields.Date.today(),
                    'fifth_state': False})

    def state_update_meet(self):
        if self.meeting == False:
            raise UserError(_('Please select Meeting Type.'))
        else:
            self.write({'state': '2a_online_meet_status'})

    def state_showroom_visit(self):
        if self.approximate_budget_id.id == False:
            raise UserError(_('Please enter Approximate Budget.'))
        else:
            self.write({'state': '3_showroom_visit',
                        'follow_date': fields.Date.today(),
                        'visit_date': fields.Date.today(),
                        'fifth_state': False})

    def state_quote(self):
        if self.quote_value == False:
            raise UserError(_('Please enter Quote value(RRP Value).'))
        else:
            self.write({'state': '4_quote',
                        'follow_date': fields.Date.today(),
                        'quote_date': fields.Date.today(),
                        'fifth_state': False})

    def state_5a_order_placed(self):
        if self.order_value <= 0.00:
            raise UserError(_('The value of the order value must be positive.'))
        elif self.scheme.id == False or self.anticipate_date == False:
            raise UserError(_('Please enter Scheme / Anticipated Delivery Date.'))
        else:
            self.write({'state': '5a_order_placed',
                        'type_of_order': 'token',
                        'order_date': fields.Date.today(),
                        'fifth_state': True,
                        'fifth_5a_token_state': True})

    def state_5b_order_placed(self):
        if self.order_value <= 0.00:
            raise UserError(_('The value of the order value must be positive.'))
        elif self.scheme.id == False or self.anticipate_date == False:
            raise UserError(_('Please enter Scheme / Anticipated Delivery Date.'))
        else:
            self.write({'state': '5b_order_placed',
                        'type_of_order': 'express',
                        'order_date': fields.Date.today(),
                        'fifth_state': True})

    def state_5c_order_placed(self):
        if self.order_value <= 0.00:
            raise UserError(_('The value of the order value must be positive.'))
        elif self.scheme.id == False or self.anticipate_date == False:
            raise UserError(_('Please enter Scheme / Anticipated Delivery Date.'))
        else:
            self.write({'state': '5c_order_placed',
                        'type_of_order': 'standard',
                        'order_date': fields.Date.today(),
                        'fifth_state': True})

    def state_5d_order_placed(self):
        if self.order_value <= 0.00:
            raise UserError(_('The value of the order value must be positive.'))
        elif self.scheme.id == False or self.anticipate_date == False:
            raise UserError(_('Please enter Scheme / Anticipated Delivery Date.'))
        else:
            self.write({'state': '5d_order_placed',
                        'type_of_order': 'lightning',
                        'order_date': fields.Date.today(),
                        'fifth_state': True})

    # def state_sale_order_req(self):
    #     self.write({'state': '6_sale_order_requested'})

    # def action_sale_quotations_new(self):
    #     if not self.partner_id:
    #         return self.env.ref("sale_crm.crm_quotation_partner_action").read()[0]
    #     else:
    #         return self.action_new_quotation(),self.write({'state': '6_sale_order_requested'})

    def action_sale_quotations_new(self):
        if not self.partner_id:
            raise ValidationError(_("Store Name is missing please contact Administrator"))
            # return self.env.ref("sale_crm.crm_quotation_partner_action").read()[0]
        else:
            self.write({'state': '6_sale_order_requested',
                        'sale_req_date': fields.Date.today()})
            return self.action_new_quotation()

    @api.model
    def fields_get(self, fields=None):
        fields_to_hide = ['fifth_5a_token_state']
        res = super(CrmLeadInherit, self).fields_get()
        for field in fields_to_hide:
            res[field]['selectable'] = False
        return res


class StageInherit(models.Model):
    _inherit = "crm.stage"

    is_showroom_visit = fields.Boolean('Is Show Room Visit?')
    is_followup = fields.Boolean('Is Followup?')
    is_bounce = fields.Boolean('Is Bounce?')
    is_quote = fields.Boolean('Is Quote?')


class CrmLeadLostInherit(models.TransientModel):
    _inherit = 'crm.lead.lost'
    _description = 'Get Lost Reason'

    lost_reason_id = fields.Many2one('crm.lost.reason', 'Lost Reason')

    def action_lost_reason_apply(self):
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        return leads.action_set_lost(lost_reason=self.lost_reason_id.id, state='8_bounced',
                                     bounce_date=fields.Date.today())


class CrmLeadDoc(models.Model):
    _name = "crm.doc.line"

    crm_source_id = fields.Many2one("crm.lead", string="Crm Source")
    name = fields.Char("Name", required=True)
    file_doc = fields.Binary("File")
    file_name = fields.Char('File Name')


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    customer_pan = fields.Char(string="PAN")
    phone = fields.Char(string='Mobile 1', required=True)
    mobile = fields.Char(string='Mobile 2')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=104)
    # state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', required=False, domain="[('country_id', '=?', country_id)]")n
    _sql_constraints = [('phone_uniq', 'unique (phone)', "Phone No already exists !")]

    @api.constrains('phone')
    def _check_phone_number(self):
        for rec in self:
            if rec.phone and re.match("^[0-9]\d{9}$", rec.phone) == None:
                raise ValidationError(_("Please enter valid Mobile1 number"))
            else:
                return False
        return {}

    @api.constrains('mobile')
    def _check_mobile_number(self):
        for rec in self:
            if rec.mobile and re.match("^[0-9]\d{9}$", rec.mobile) == None:
                raise ValidationError(_("Please enter valid Mobile2 number"))
            else:
                return False
        return {}

    def _compute_access(self):
        users = self.env['res.users'].sudo().search([('partner_id', '=', self.id)], limit=1)
        #blpl
        if users.has_group('ind_access_extend.group_national_head_admin'):
            self.is_national_head = True
        else:
            self.is_national_head = False
        if users.has_group('ind_access_extend.group_regional_bdm_admin'):
            self.is_regional_bdm = True
        else:
            self.is_regional_bdm = False
        if users.has_group('ind_access_extend.group_bdm_admin'):
            self.is_bdm = True
        else:
            self.is_bdm = False
        if users.has_group('ind_access_extend.group_blpl_service_manager_admin'):
            self.is_blpl_service_manager = True
        else:
            self.is_blpl_service_manager = False
        if users.has_group('ind_access_extend.group_blpl_service_engineer_admin'):
            self.is_blpl_service_engineer = True
        else:
            self.is_blpl_service_engineer = False
        if users.has_group('ind_access_extend.group_blpl_store_team_admin'):
            self.is_blpl_store_team = True
        else:
            self.is_blpl_store_team = False
        if users.has_group('ind_access_extend.group_interior_consultant_admin'):
            self.is_interior_consultant = True
        else:
            self.is_interior_consultant = False
        if users.has_group('ind_access_extend.group_sales_team_lead_admin'):
            self.is_sales_team_lead = True
        else:
            self.is_sales_team_lead = False
        if users.has_group('ind_access_extend.group_sales_lead_admin'):
            self.is_sales_lead = True
        else:
            self.is_sales_lead = False
        if users.has_group('ind_access_extend.group_blpl_service_tech_admin'):
            self.is_blpl_service_techinician = True
        else:
            self.is_blpl_service_techinician = False
        if users.has_group('ind_access_extend.group_dealer_associates_admin'):
            self.is_deal_associate = True
        else:
            self.is_deal_associate = False
        if users.has_group('ind_access_extend.group_blpl_associates_admin'):
            self.is_blpl_associate_id = True
        else:
            self.is_blpl_associate_id = False
        #End BLPL
        #Franchisee
        if users.has_group('ind_access_extend.group_national_head_admin'):
            self.is_franchisee_national_head = True
        else:
            self.is_franchisee_national_head = False

        if users.has_group('ind_access_extend.group_franchisee_rm_admin'):
            self.is_franchisee_rm = True
        else:
            self.is_franchisee_rm = False
        if users.has_group('ind_access_extend.group_franchisee_bdm_admin'):
            self.is_franchisee_bdm = True
        else:
            self.is_franchisee_bdm = False
        if users.has_group('ind_access_extend.group_franchisee_service_manager_admin'):
            self.is_franchisee_blpl_service_manager = True
        else:
            self.is_franchisee_blpl_service_manager = False
        if users.has_group('ind_access_extend.group_franchisee_service_engineer_admin'):
            self.is_franchisee_blpl_service_engineer = True
        else:
            self.is_franchisee_blpl_service_engineer = False
        if users.has_group('ind_access_extend.group_franchisee_owner_admin'):
            self.is_franchisee_owner = True
        else:
            self.is_franchisee_owner = False
        if users.has_group('ind_access_extend.group_sales_cordinator_admin'):
            self.is_sales_cordinators = True
        else:
            self.is_sales_cordinators = False
        if users.has_group('ind_access_extend.group_sales_manager_admin'):
            self.is_sales_managere = True
        else:
            self.is_sales_managere = False
        if users.has_group('ind_access_extend.group_sales_executive_admin'):
            self.is_sales_executive = True
        else:
            self.is_sales_executive = False
        if users.has_group('ind_access_extend.group_service_technician_admin'):
            self.is_service_technician = True
        else:
            self.is_service_technician = False
        if users.has_group('ind_access_extend.group_dealer_admin'):
            self.is_franchisee_dealer = True
        else:
            self.is_franchisee_dealer = False
        if users.has_group('ind_access_extend.group_associates_admin'):
            self.is_associates = True
        else:
            self.is_associates = False




    # national_head_id = fields.Many2one("res.partner", string="National Head", tracking=True)
    is_national_head = fields.Boolean(string="Is National Head", compute="_compute_access")
    is_regional_bdm = fields.Boolean(string="Is RM Direct", compute="_compute_access")
    is_bdm = fields.Boolean(string="Is BDM Direct", compute="_compute_access")
    is_blpl_service_manager = fields.Boolean(string="Is BLPL Service Manager", compute="_compute_access")
    is_blpl_service_engineer = fields.Boolean(string="Is Service Engineer", compute="_compute_access")
    is_blpl_store_team = fields.Boolean(string="Is BLPL Store Team", compute="_compute_access")
    is_interior_consultant = fields.Boolean(string="Is Interior Consoultants", compute="_compute_access")
    is_sales_team_lead = fields.Boolean(string="Is Sales Team Lead", compute="_compute_access")
    is_sales_lead = fields.Boolean(string="Is Sales Lead", compute="_compute_access")
    is_blpl_service_techinician = fields.Boolean(string="Is Service Techinician", compute="_compute_access")
    is_deal_associate = fields.Boolean(string="Is Dealer", compute="_compute_access")
    is_blpl_associate_id = fields.Boolean(string="Is Associates", compute="_compute_access")



    # blpl_master_id = fields.Many2one("blpl.master", string="BLPL Master", tracking=True)
    # franchisee_master_ids = fields.Many2many("franchisee.master", string="Franchisee Master", tracking=True)
    is_franchisee_national_head = fields.Boolean(string="Is National Head", compute="_compute_access")
    is_franchisee_rm = fields.Boolean(string="Is RM", compute="_compute_access")
    is_franchisee_bdm = fields.Boolean(string="Is BDM", compute="_compute_access")
    is_franchisee_blpl_service_manager = fields.Boolean(string="Is BLPL Service Manager", compute="_compute_access")
    is_franchisee_blpl_service_engineer = fields.Boolean(string="Is Service Engineer", compute="_compute_access")
    is_franchisee_owner = fields.Boolean(string="Is Franchisee Owner", compute="_compute_access")
    is_sales_cordinators = fields.Boolean(string="Is Sales Cordinator", compute="_compute_access")
    is_sales_managere = fields.Boolean(string="Is Sales Manager", compute="_compute_access")
    is_sales_executive = fields.Boolean(string="Is Sales Executive", compute="_compute_access")
    is_service_technician = fields.Boolean(string="Is Service Techinician", compute="_compute_access")
    is_franchisee_dealer = fields.Boolean(string="Is Dealer", compute="_compute_access")
    is_associates = fields.Boolean(string="Is Associates", compute="_compute_access")




    # regional_bdm_ids = fields.Many2many('res.users', string="Regional BDM")
    # bdm_ids = fields.Many2many("res.users", string="BDM", tracking=True)
    #
    # blpl_store_team_ids = fields.Many2many("res.users", string="BLPL Store Team", tracking=True)
    # interior_consultant_ids = fields.Many2many("res.users", string="Interior Consoultants", tracking=True)
    # sales_team_lead_ids = fields.Many2many("res.users   ", string="Sales Team Lead", tracking=True)
    # sales_lead_ids = fields.Many2many("res.users", string="Sales Lead", tracking=True)
    # deal_associate_ids = fields.Many2many("res.users", string="Dealer / Associate", tracking=True)

class ResPartnerCron(models.Model):

    _name = 'res.partner.cron'

    def res_partner_company_cron(self):
        for users_rec in self.env['res.users'].sudo().search([]):
            for partner_rec in users_rec.partner_id:
                if not partner_rec.company_id:
                    partner_rec.update({
                        'company_id': users_rec.company_id.id})
                # else:
                #     partner_rec.update({
                #         'company_id': users_rec.company_id.id})




class OpportunityMaster(models.Model):
    _name = "opportunity.master"

    name = fields.Char('Name')

    def action_opportunity(self):
        self.ensure_one()
        return {
            'name': _('Opportunity Master'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'opportunity.master',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

class BudgetMaster(models.Model):
    _name = "budget.master"

    name = fields.Char('Name')

class SchemeMaster(models.Model):
    _name = "scheme.master"


    name = fields.Char('Scheme Name')
    doc = fields.Binary("Scheme File", required=True)
    doc_name = fields.Char('File Name')
    from_date = fields.Datetime(string="Start Date")
    to_date = fields.Datetime(string="End Date")
    # date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    # from_date = fields.Date('Start Date')
    # to_date = fields.Date('End Date')
    discount = fields.Float('Discount')
    partner_ids = fields.Many2many('res.partner', string="Based on Dealers", required=True)
    # scheme_active = fields.Boolean(string="Active")

    def name_get(self):
        result = []
        for scheme in self:
            name = scheme.name + '-' + str(scheme.discount) + '%'
            result.append((scheme.id, name))
        return result


    @api.constrains('rule_date_to', 'from_date', 'discount')
    def _check_rule_date_from(self):
        if any(applicability for applicability in self
               if applicability.to_date and applicability.from_date
                  and applicability.to_date < applicability.from_date):
            raise ValidationError(_('The start date must be before the end date'))
        if self.discount <= 0.00:
            raise ValidationError(_('The discount should be positive'))



    # @api.model
    # def create(self, values):
    #     if values['discount'] <= 0.00:
    #         raise UserError(_('The value of the discount must be positive1.'))
    #     if not (values['from_date'] or values['to_date']):
    #         raise UserError(_('Please Select From/To date.'))
    #     if values['partner_ids'] == False:
    #         warning_mess = {
    #             'title': _('There is no Dealer!'),
    #             'message': _(
    #                 'Discount is applicable for all dealers'),
    #         }
    #         return {'warning': warning_mess}
    #     return super(SchemeMaster, self).create(values)
    #
    # @api.onchange('discount', 'partner_ids')
    # def _onchange_discount(self):
    #     if self.name and self.discount <= 0.00:
    #         raise UserError(_('The value of the discount must be positive2.'))
    #     if self.name and not (self.from_date or self.to_date):
    #         raise UserError(_('Please Select From/To date.'))
    #     if self.name and not self.partner_ids:
    #         warning_mess = {
    #             'title': _('There is no Dealer!'),
    #             'message': _(
    #                 'Discount is applicable for all dealers'),
    #         }
    #         return {'warning': warning_mess}
    #     return {}

#     status_id = fields.Many2one('crm.lead.status', string='Staus', default=1)
#
#
#
# class CrmLeadStatus(models.Model):
#     _name = "crm.lead.status"
#     _description = 'Status for CRM'
#
#     name = fields.Char('Status')
#     id = fields.integer('Id')
class PartnerBindingInherit(models.TransientModel):
    """
        Handle the partner binding or generation in any CRM wizard that requires
        such feature, like the lead2opportunity wizard, or the
        phonecall2opportunity wizard.  Try to find a matching partner from the
        CRM model's information (name, email, phone number, etc) or create a new
        one on the fly.
        Use it like a mixin with the wizard of your choice.
    """

    _inherit = 'crm.partner.binding'
    _description = 'Partner linking/binding in CRM wizard'

    action = fields.Selection([
        ('create', 'Create a new Dealer'),
        ('exist', 'Link to an existing Dealer'),
        ('nothing', 'Do not link to a Dealer')
    ], 'Related Dealer', required=True)

class BlplMaster(models.Model):
    _name = "blpl.master"

    # def _group_national_head_domain(self):
    #     group = self.env.ref('ind_access_extend.group_national_head_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []

    # def group_regional_head_domain(self):
    #     group = self.env.ref('ind_access_extend.group_regional_bdm_admin', raise_if_not_found=False)
    #     return [('groups_id', 'in', group.ids)] if group else []


    national_head_id = fields.Many2one("res.users", string="National Head", tracking=True, domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_national_head_admin").id)])
    # category_id = fields.Many2one("res.partner", string="1")
    # partner_id = fields.Many2one("res.partner", string="2")
    regional_bdm_ids = fields.Many2many('res.users', string='RM Direct', domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_regional_bdm_admin").id)])
    bdm_ids = fields.Many2many(relation='bdm_rel', comodel_name='res.users', column1='category_id', column2='partner_id', string='BDM Direct', domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_bdm_admin").id)])
    blpl_service_manager_ids = fields.Many2many(relation='blpl_service_manager_rel', comodel_name='res.users', column1='blpl_service_manager1_id', column2='blpl_service_manager2_id', string='BLPL Service Manager', domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_blpl_service_manager_admin").id)])
    blpl_service_engineer_ids = fields.Many2many(relation='blpl_service_engg_rel', comodel_name='res.users', column1='blpl_service_engg1_id', column2='blpl_service_engg2_id', string='Service Engineer', domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_blpl_service_engineer_admin").id)])
    name = fields.Char("Bethliving Store Profile")


    blpl_store_team_ids = fields.Many2many(relation='blpl_rel', comodel_name="res.users", column1='team_id', column2='bd2_id', string="Store Manager", domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_blpl_store_team_admin").id)])
    interior_consultant_ids = fields.Many2many(relation='interior_rel', comodel_name="res.users", column1='interior1_id', column2='interior2_id', string="Interior Consoultant", domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_interior_consultant_admin").id)])
    sales_team_lead_ids = fields.Many2many(relation='sales_team_rel', comodel_name="res.users", column1='sales_team1_id', column2='sales_team2_id', string="Sales Team Lead", domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_sales_team_lead_admin").id)])
    sales_lead_ids = fields.Many2many(relation='sales_lead_rel', comodel_name="res.users", column1='sales_lead1_id',column2='sales_lead2_id', string="Sales Lead", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_sales_lead_admin" ).id)])

    blpl_service_techinician_ids = fields.Many2many(relation='blpl_service_techinician_rel', comodel_name="res.users", column1='blpl_service_techinician1_id',column2='blpl_service_techinician2_id', string="Service Techinician", domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_blpl_service_tech_admin").id)])

    deal_associate_ids = fields.Many2many(relation='deal_associate_rel', comodel_name="res.users", column1='associate1_id', column2='associate2_id', string="Dealer", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_dealer_associates_admin").id)])
    blpl_associate_ids = fields.Many2many(relation='blpl_associate_rel', comodel_name="res.users", column1='blpl_associate1_id', column2='blpl_associate2_id', string="Associates", domain=lambda self: [("groups_id", "=", self.env.ref("ind_access_extend.group_blpl_associates_admin").id)])


    # def write(self, vals):
    #     rslt = super(BlplMaster, self).write(vals)
    #     for users_rec in self.env['res.users'].search([]):
    #         partner_record = self.env['res.partner'].search([('id', '=', users_rec.partner_id.id)])
    #         for partner_rec in partner_record:
    #             if users_rec.id in self.regional_bdm_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 partner_rec.write({
    #                             'is_regional_bdm': True,
    #                             'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 partner_rec.write({
    #                             'is_regional_bdm': False,
    #                             'blpl_master_id': False})
    #             if users_rec.id in self.bdm_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_bdm_admin').id)]})
    #                 partner_rec.write({
    #                     'is_bdm': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_bdm_admin').id)]})
    #                 partner_rec.write({
    #                     'is_bdm': False,
    #                     'blpl_master_id': False})
    #             if users_rec.id in self.blpl_store_team_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_blpl_store_team_admin').id)]})
    #                 partner_rec.write({
    #                     'is_blpl_store_team': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_blpl_store_team_admin').id)]})
    #                 partner_rec.write({
    #                     'is_blpl_store_team': False,
    #                     'blpl_master_id': False})
    #             if users_rec.id in self.interior_consultant_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_interior_consultant_admin').id)]})
    #                 partner_rec.write({
    #                     'is_interior_consultant': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_interior_consultant_admin').id)]})
    #                 partner_rec.write({
    #                     'is_interior_consultant': False,
    #                     'blpl_master_id': False})
    #             if users_rec.id in self.sales_team_lead_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_sales_team_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_team_lead': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_sales_team_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_team_lead': False,
    #                     'blpl_master_id': False})
    #             if users_rec.id in self.sales_lead_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_sales_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_lead': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_sales_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_lead': False,
    #                     'blpl_master_id': False})
    #             if users_rec.id in self.deal_associate_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_dealer_associates_admin').id)]})
    #                 partner_rec.write({
    #                     'is_deal_associate': True,
    #                     'blpl_master_id': self.id})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_dealer_associates_admin').id)]})
    #                 partner_rec.write({
    #                     'is_deal_associate': False,
    #                     'blpl_master_id': False})

        # for partner_rec in self.env['res.partner'].search([]):
        #     if partner_rec.id in self.regional_bdm_ids.ids:
        #          partner_rec.write({
        #             'is_regional_bdm': True })
        #     else:
        #         partner_rec.write({
        #             'is_regional_bdm': False})
        #     if partner_rec.id in self.bdm_ids.ids:
        #         partner_rec.write({
        #             'is_bdm': True })
        #     else:
        #         partner_rec.write({
        #             'is_bdm': False})
        #     if partner_rec.id in self.blpl_store_team_ids.ids:
        #         partner_rec.write({
        #             'is_blpl_store_team': True })
        #     else:
        #         partner_rec.write({
        #             'is_blpl_store_team': False})
        #     if partner_rec.id in self.interior_consultant_ids.ids:
        #         partner_rec.write({
        #             'is_interior_consultant': True })
        #     else:
        #         partner_rec.write({
        #             'is_interior_consultant': False})
        #     if partner_rec.id in self.sales_team_lead_ids.ids:
        #         partner_rec.write({
        #             'is_sales_team_lead': True })
        #     else:
        #         partner_rec.write({
        #             'is_sales_team_lead': False})
        #     if partner_rec.id in self.sales_lead_ids.ids:
        #         partner_rec.write({
        #             'is_sales_lead': True })
        #     else:
        #         partner_rec.write({
        #             'is_sales_lead': False})
        #     if partner_rec.id in self.deal_associate_ids.ids:
        #         partner_rec.write({
        #             'is_deal_associate': True })
        #     else:
        #         partner_rec.write({
        #             'is_deal_associate': False})

        # return rslt

    # @api.model
    # def create(self, values):
    #     blpl = super(BlplMaster, self).create(values)
    #     for users_rec in self.env['res.users'].search([]):
    #         print ("111111111111111")
    #         partner_record = self.env['res.partner'].search([('id', '=', users_rec.partner_id.id)])
    #         for partner_rec in partner_record:
    #             print ("222222222222222")
    #             if users_rec.id in self.regional_bdm_ids.ids:
    #                 print ("33333333333333")
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 partner_rec.write({
    #                             'is_regional_bdm': True })
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 partner_rec.write({
    #                             'is_regional_bdm': False})
    #             if users_rec.id in self.bdm_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_bdm_admin').id)]})
    #                 partner_rec.write({
    #                     'is_bdm': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_bdm_admin').id)]})
    #                 partner_rec.write({
    #                     'is_bdm': False})
    #             if users_rec.id in self.blpl_store_team_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_blpl_store_team_admin').id)]})
    #                 partner_rec.write({
    #                     'is_blpl_store_team': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_blpl_store_team_admin').id)]})
    #                 partner_rec.write({
    #                     'is_blpl_store_team': False})
    #             if users_rec.id in self.interior_consultant_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_interior_consultant_admin').id)]})
    #                 partner_rec.write({
    #                     'is_interior_consultant': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_interior_consultant_admin').id)]})
    #                 partner_rec.write({
    #                     'is_interior_consultant': False})
    #             if users_rec.id in self.sales_team_lead_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_sales_team_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_team_lead': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_sales_team_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_team_lead': False})
    #             if users_rec.id in self.sales_lead_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_sales_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_lead': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_sales_lead_admin').id)]})
    #                 partner_rec.write({
    #                     'is_sales_lead': False})
    #             if users_rec.id in self.deal_associate_ids.ids:
    #                 users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_dealer_associates_admin').id)]})
    #                 partner_rec.write({
    #                     'is_deal_associate': True})
    #             else:
    #                 users_rec.write(
    #                     {'groups_id': [(3, self.env.ref('ind_access_extend.group_dealer_associates_admin').id)]})
    #                 partner_rec.write({
    #                     'is_deal_associate': False})
    #     return blpl

class FranchiseeMaster(models.Model):
    _name = "franchisee.master"

    # franchisee_national_head_id = fields.Many2one(relation='franchisee_national_rel', comodel_name="res.users", column1='fnational1_id',
    #                           column2='fnational2_id', string="National Head", tracking=True)
    franchisee_national_head_id = fields.Many2one(comodel_name="res.users", string="National Head", tracking=True, domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_national_head_admin").id)])
    franchisee_rm_ids = fields.Many2many(relation='franchisee_rm_rel', comodel_name="res.users", column1='rm1_id',
                              column2='rm2_id', string="RM", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_franchisee_rm_admin").id)])
    franchisee_bdm_ids = fields.Many2many(relation='franchisee_bdm_rel', comodel_name="res.users", column1='fbdm1_id',
                                          column2='fbdm2_id',
                                          string="BDM", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_franchisee_bdm_admin").id)])
    franchisee_blpl_service_manager_ids = fields.Many2many(relation='franchisee_service_man_rel', comodel_name="res.users", column1='fservice_manager1_id',
                                          column2='fservice_manager2_id',
                                          string="BLPL Service Manager", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_franchisee_service_manager_admin").id)])
    franchisee_blpl_service_engineer_ids = fields.Many2many(relation='franchisee_service_engg_rel', comodel_name="res.users",
                                                           column1='fservice_engg1_id',
                                                           column2='fservice_engg2_id',
                                                           string="Service Engineer", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_franchisee_service_engineer_admin").id)])
    name = fields.Char("Team Name", required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    franchisee_profile_id = fields.Many2one('res.partner', string='Franchisee Profile', store=True, related='company_id.partner_id',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    franchisee_owner_ids = fields.Many2many(relation='franchisee_owner_rel', comodel_name="res.users", column1='fowner1_id', column2='fowner2_id', string="Franchisee Owner", tracking=True, domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_franchisee_owner_admin").id)])
    sales_cordinators_ids = fields.Many2many('res.users', string='Sales Cordinator', domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_sales_cordinator_admin").id)])
    sales_managere_ids = fields.Many2many(relation='franchisee_manager_rel', comodel_name="res.users", column1='manager1_id',
                                           column2='manager2_id', string="Sales Manager", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_sales_manager_admin").id)])
    sales_executive_ids = fields.Many2many(relation='franchisee_executive_rel', comodel_name="res.users",
                                               column1='executive1_id', column2='executive2_id',
                                               string="Sales Executive", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_sales_executive_admin").id)])
    service_technician_ids = fields.Many2many(relation='franchisee_service_rel', comodel_name="res.users",
                                           column1='service1_id', column2='service2_id', string="Service Techinician", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_service_technician_admin").id)])
    franchisee_dealer_ids = fields.Many2many(relation='franchisee_dealer_rel', comodel_name="res.users", column1='dealer1_id',
                                      column2='dealer2_id', string="Dealer", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_dealer_admin").id)])
    associates_ids = fields.Many2many(relation='franchisee_associates_rel', comodel_name="res.users",
                                          column1='franchisee_associate1_id', column2='franchisee_associate2_id', string="Associates", domain=lambda self: [("groups_id", "=", self.env.ref( "ind_access_extend.group_associates_admin").id)])

    # @api.onchange('sales_cordinators_ids')
    # def _onchange_sales_cordinators_ids(self):
    #     for franchisee_rec in self.env['franchisee.master'].search([]):
    #         print (franchisee_rec.sales_cordinators_ids, self.sales_cordinators_ids.ids, "11111111111111111111111")
    #         if franchisee_rec.sales_cordinators_ids in self.sales_cordinators_ids.ids:
    #             print ("22222222222222222222")
    #             raise UserError(_('This user is already mapped with another team.'))
    # def write(self, vals):
    #     rslt = super(FranchiseeMaster, self).write(vals)
    #     for users_rec in self.env['res.users'].search([]):
    #         partner_record = self.env['res.partner'].search([('id', '=', users_rec.partner_id.id)])
    #         for partner_rec in partner_record:
    #             if users_rec.id in self.sales_cordinators_ids.ids:
    #                 # users_rec.write({'groups_id': [(4, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 # print ("1111111111111111111111")
    #                 partner_rec.write({
    #                             'franchisee_master_ids': [(4,  self.id)]})
    #                 # [(6, 0, ids_cus)]
    #             else:
    #                 # users_rec.write(
    #                 #     {'groups_id': [(3, self.env.ref('ind_access_extend.group_regional_bdm_admin').id)]})
    #                 partner_rec.write({
    #                             'franchisee_master_ids': [(3,  self.id)]})
    #     return rslt