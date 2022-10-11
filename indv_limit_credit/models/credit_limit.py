# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


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
        ('cancel','Cancel')],string="State", default="draft", tracking=True)
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        tracking=True)
    vat = fields.Char(
        string="VAT",
        related="partner_id.vat")
    current_user_id = fields.Many2one(
        'res.users',
        'Current User',
        default=lambda self: self.env.user)
    fee_numbers = fields.Integer(
        string="Fee",
        tracking=True)
    credit_type = fields.Selection([
        ('direct','Direct'),
        ('third','Third')],string="Credit type", tracking=True)
    percentage = fields.Float(
        string="percentage",
        tracking=True)
    credit_amount_total = fields.Float(
        string="Total",
        compute="calculate_credit",
        tracking=True)
    entity_type = fields.Selection([
        ('bank','Bank'),
        ('other','Other')],string="Entity type", tracking=True)
    bank_id = fields.Many2one(
        'res.bank',
        string="Bank",
        tracking=True)
    entity_id = fields.Many2one(
        'res.partner',
        string="Entity",
        tracking=True)
    is_approval_credit = fields.Boolean(
        string="Aproval credit")
    is_cancel_credit = fields.Boolean(
        string="Cancel credit")
    credit_line_ids = fields.One2many(
        'credit.limit.lines',
        'credit_id',
        string="Quotas")
    description = fields.Char(
        string="Description")
    date = fields.Date(
        string="Payment Start Date",
        required=True,
        default=fields.Date.today())
    installment = fields.Integer(
        string="No Of Installments",
        default=1,
        help="Number of installments")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company)


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
        self.write({
            'state': 'approved',
            'is_approval_credit': True,
            })

    def write_cancel_state(self):
        if not (self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group') or self.env.user.has_group('indv_limit_credit.credit_limit_approval_manager_group')):
            raise UserError(_('Only credit Managers can approve credits'))
        self.write({
            'state': 'cancel',
            'is_cancel_credit': True,
            })

    @api.constrains('partner_id','state')
    def check_credit(self):
        self.ensure_one()
        same_number_recs = self.search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'approved'),]) - self
        if same_number_recs:
            raise ValidationError(_("This partner already a credit in current: %s" % self.partner_id.name))

    @api.constrains('fee_numbers')
    def check_faa(self):
        for record in self:
            if record.fee_numbers < 0:
                raise ValidationError(_("The faa numbers can not 0: %s" % record.fee_numbers))

    @api.constrains('percentage')
    def check_percentaje(self):
        for record in self:
            if record.percentage < 0:
                raise ValidationError(_("The percentage can not 0: %s" % record.percentage))

    @api.constrains('credit_amount')
    def check_credit_amount(self):
        for record in self:
            if record.credit_amount < 0:
                raise ValidationError(_("The credit amount can not 0: %s" % record.credit_amount))

    @api.depends(
        'credit_amount',
        'percentage',
        'fee_numbers')
    def calculate_credit(self):
        for record in self:
            if record.fee_numbers > 0 and record.percentage > 0:
                credit_value = record.credit_amount
                tasa = record.percentage / 100
                quota = (1 - (1 + tasa)** tasa)
                div = quota / record.percentage
                record.credit_amount_total = credit_value / div
            else:
                record.credit_amount_total = 0


    def compute_credits(self):
        for credit in self:
            credit.credit_line_ids.unlink()
            date_start = datetime.strptime(str(credit.date), '%Y-%m-%d')
            for i in range(1, credit.fee_numbers + 1):
                self.env['credit.limit.lines'].create({
                    'date': date_start,
                    'item': i,
                    'credit_id': credit.id,
                    'name': 'CUOTA #' + '' + str(i)
                    })
                date_start = date_start + relativedelta(months=1)
        return True





class CreditLimitLines(models.Model):
    _name = 'credit.limit.lines'
    _description = 'Credit limit lines'

    name = fields.Char(
        string="Name")
    credit_id = fields.Many2one(
        'credit.limit',
        string="Credit")
    credit_amount = fields.Float(
        string="Credit amount")
    date = fields.Date(
        string="Date")
    item = fields.Integer(
        string="Item")
    description = fields.Char(
        string="Description")
    installment = fields.Integer(
        string="No Of Installments",
        default=1,
        help="Number of installments")
