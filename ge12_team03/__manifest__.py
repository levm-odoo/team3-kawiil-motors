{
    "name": "ge12_team03",
    "summary": "ge12_team03",
    "description": """
        tasks GE12
        GE12: Automatic Portal Account Creation
        K'awiil Motors wants their customers to be able to view information about 
        their motorcycles on the customer portal. As their number of customers increases, 
        manually creating new portal accounts becomes too time consuming. They want a new portal account to be automatically generated for new customers. They also want customers to receive an email when this account is created, providing instructions and credentials for accessing their registration data.""",
    "version": "1.0.0",
    "category": "Kauil/Users",
    "license": "OPL-1",
    "depends": ["motorcycle_registry", "portal", 'ge07_team03',],
    'data': [
        'data/mail_template.xml',
    ],
    "author": "Odoo, Inc.",
    "website": "www.odoo.com",
    "application": False,
}
