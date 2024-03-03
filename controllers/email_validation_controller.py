from odoo import http, _
from odoo.http import request

class EmailValidationController(http.Controller):

    @http.route(['/email/<string:email>/<string:email_confirmation_token>'], type='http', auth="public")
    def portal_my_invoice_detail(self, email, email_confirmation_token, **kw):
        confirmation = request.env['partner.email.confirmation'].sudo().search([['state', '=', 'pending'], ['name', '=', email], ['confirmation_token', '=', email_confirmation_token]])
        if confirmation:
            confirmation._confirm_email()
            return "<h1>Email Confirmed</h1>"
        return "<h1>Link are expired or alredy has been used</h1>"