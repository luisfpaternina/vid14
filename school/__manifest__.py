##########################################################################################
#
# Ing.Luis Felipe Paternina
# Odoo Dev
#
# lfpaternina93@gmail.com
#
# +573215062353
#
# Bogota,Colombia
#
############################################################################################

{
    'name': 'School',

    "summary": """This module is educational, which allows you to keep track of teachers, students, enrollment, among other things.""",

    'version': '14.0',

    'author': "Luis Felipe Paternina",

    'website': "https://github.com/luisfpaternina",

    'category': 'learning',

    'depends': [

        'base',
        'base_address_city',

    ],

    'data': [

        'security/ir.model.access.csv',
        'security/security.xml',      
        'views/school.xml',
        'views/students.xml',
        'views/teachers.xml',
        'views/courses.xml',
        'views/area.xml',
        'views/settings.xml',
        'views/license_plates.xml',
        #'reports/report_license_plates.xml',
              
    ],
    
    "images": [
        'static/description/school.png'
    ],
    

    "application": False,
    "installable": True,
    "auto_install": False,

}
