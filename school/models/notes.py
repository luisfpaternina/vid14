# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL


from odoo import models, fields,_

class Notes(models.Model):

    _name = "notes"
    _description = "Notes"

    
    name = fields.Char(string='Name', required=True, tracking=True)
    
    
    

 
   







    
    
    