from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class QuestionsMaster(models.Model):
    _name = 'questions.master'
    _inherit = ['mail.thread']
    _description = "Question Master"

    product_group_id = fields.Many2one('product_group.master',string="Product Group")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    questions_line_ids = fields.One2many('questions.line', 'header_id')

class QuestionsLine(models.Model):
	_name = 'questions.line'
	_description = "Set of Questions"

	name = fields.Text("Questions")
	header_id = fields.Many2one('questions.master')