# -*- coding: utf-8 -*-
##################################################################################################################################
#
# ING.LUIS FELIPE PATERNINA VITAL
#  
# Correo: lfpaternina93@gmail.com
#
#
# Celular: +573046079971 or +573215062353
#
# Bogotá,Colombia
#
###################################################################################################################################


from odoo import models, fields, api,_


class LicensePlates(models.Model):

    _name = "license.plates"
    _description = "License plates"

    
    name = fields.Char(string="Nombre", readonly=True, required=True, copy=False, tracking=True, default='New')
    student_id = fields.Many2one('students', string="Student")
    course = fields.Char(string="Course")
    create_date = fields.Datetime('Create Date', tracking=True, default= fields.Datetime().now())
    identification_number = fields.Char(string="Identification number", tracking=True, related="student_id.identification_number")
    blood_group = fields.Selection(string="Blood Group",related="student_id.blood_group")
    identification_type = fields.Selection(string="Identification Type", related="student_id.identification_type")
    address = fields.Char(string="Address", related="student_id.address")
    cellphone = fields.Char(string="Phone", related="student_id.cellphone")
    neighborhood = fields.Char(string="Neighborhood", related="student_id.neighborhood")
    gender = fields.Selection(string="Gender", related="student_id.gender")
    email = fields.Char(string="Email", related="student_id.email")



    #Secuencia para las matriculas de los estudiantes
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('license.plates') or 'New'

        result = super(LicensePlates, self).create(vals)
        return result


    #crear nuevo registro en sale.order
    def create_record_in_Sale_order(self):

        vals = {

           'name': self.name,
           'partner_id': self.student_id.id,
           'validity_date': self.create_date,
           
		}
        self.env['sale.order'].create(vals)






    
    
    

 
   







    
    
    