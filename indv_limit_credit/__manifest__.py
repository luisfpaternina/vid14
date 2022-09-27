{
    'name': 'Credit limit',

    'version': '14.0.0.0',

    'author': "Luis Felipe Paternina",

    'contributors': ['Luis Felipe Paternina'],

    'website': "",

    'category': 'account',

    'depends': [

       
        'base',
        'sale_management',
        'account_accountant',
        'contacts',

    ],

    'data': [
       
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/credit_limit.xml',
                   
    ],
    'installable': True
}
