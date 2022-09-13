# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL


from odoo import models, fields,_

class Area(models.Model):

    _name = "area"
    _description = "Areas"

    
    name = fields.Char(string='Name', required=True, tracking=True)
    
    
    

 
   







    
    
    