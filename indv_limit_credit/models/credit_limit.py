# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditLimit(models.Model):
    _name = 'credit.limit'
    _inherit = 'mail.thread'
    _description = 'Credit limit'

    name = fields.Char(
        string="Name",
        readonly=True,
        required=True,
        copy=False,
        default='New')
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
    vat = fields.Char(
        string="VAT",
        related="partner_id.vat")

    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('credit.limit') or 'New'       

        result = super(CreditLimit, self).create(vals)
        return result



class CreditLimitLines(models.Model):
    _name = 'credit.limit.lines'
    _description = 'Credit limit lines'

    name = fields.Char(
        string="Name")
