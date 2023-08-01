{
    "name": "GE10_Team03",
    "summary": "Motorcycle Registry Snippets",
    "description": """
    Motorcycle Snippets
This Module is used to generate new snippets for the website module to display motorcycle information
    """,
    "version": "1.0.0",
    "category": "Kauil/Snippets",
    "license": "OPL-1",
    "depends": ["website","website_profile","motorcycle_registry"],
    'assets': {
        'web.assets_frontend': [          
            'ge10_team03/static/src/scss/motorcycle.scss',
            'ge10_team03/static/src/js/motorcycle.js'
        ]
    },
    "data": ["views/snippet_templates.xml",
    ],
    "author": "Odoo, Inc",
    "website": "www.odoo.com",
    "application": False,
}
