# -*- coding: utf-8 -*-
#BY: LUIS FELIPE PATERNINA VITAL


from odoo import models, fields,_

class Settings(models.Model):

    _name = "settings"
    _description = "Settings"

    
    name = fields.Char(string='Name', required=True, tracking=True)
    
    
    

 
   







    
    
    