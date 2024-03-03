{
    'name': 'Contacts Email Validation',
    'version': '1.0',
    'description': 'Validate emails of partners',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/email_disify_result_views.xml',
        'views/email_confirmation_views.xml',
        'views/menuitems.xml',
        'data/confirmation_email_template.xml',
        'data/cron.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}