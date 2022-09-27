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
        ('current','Validation'),
        ('approved','Approved'),
        ('done','Done'),
        ('cancel','Cancel')],string="State", default="draft")
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner")
    vat = fields.Char(
        string="VAT",
        related="partner_id.vat")
    current_user_id = fields.Many2one(
        'res.users',
        'Current User',
        default=lambda self: self.env.user)
    fee_numbers = fields.Integer(
        string="Fee")
    credit_type = fields.Selection([
        ('direct','Direct'),
        ('third','Third')],string="Credit type")
    percentage = fields.Float(
        string="percentage")
    credit_amount_total = fields.Float(
        string="Total")
    entity_type = fields.Selection([
        ('bank','Bank'),
        ('other','Other')],string="Entity type")
    bank_id = fields.Many2one(
        'res.bank',
        string="Bank")
    entity_id = fields.Many2one(
        'res.partner',
        string="Entity")

    @api.onchange('name')
    def _upper_name(self):        
        self.name = self.name.upper() if self.name else False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('credit.limit') or 'New'       

        result = super(CreditLimit, self).create(vals)
        return result

    def write_current_state(self):
        if not (self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group') or self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group')):
            raise UserError(_('Only credit Managers can approve credits'))
        self.write({'state': 'current'})

    def write_approval_state(self):
        if not (self.env.user.has_group('indv_limit_credit.credit_limit_manager_group') or self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group')):
            raise UserError(_('Only credit Managers can approve credits'))
        self.write({'state': 'approved'})

    def write_cancel_state(self):
        if not (self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group') or self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group')):
            raise UserError(_('Only credit Managers can approve credits'))
        self.write({'state': 'cancel'})

    @api.constrains('partner_id','state')
    def check_credit(self):
        self.ensure_one()
        same_number_recs = self.search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', self.state),]) - self
        if same_number_recs:
            raise ValidationError(_("This partner already a credit in current: %s" % record.partner_id.name))



class CreditLimitLines(models.Model):
    _name = 'credit.limit.lines'
    _description = 'Credit limit lines'

    name = fields.Char(
        string="Name")
    credit_id = fields.Many2one(
        'credit.limit',
        string="Credit")
