# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditLimit(models.Model):
    _name = 'credit.limit'
    _inherit = 'mail.thread'
    _description = 'Credit limit'

    name = fields.Char(
        string="Name")
    credit_amount = fields.Float(
        string="Credit amount")
    state = fields.Selection([
        ('draft','Draft'),
        ('current','Current'),
        ('approved','Approved'),
        ('done','Done')],string="State")
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner")

    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False
