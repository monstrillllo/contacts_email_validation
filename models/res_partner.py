from odoo import _, api, fields, models
from odoo.exceptions import UserError
import requests
import re
import logging

_logger = logging.getLogger(__name__)

TIMEOUT = 10
DISIFY_URL_PATTERN = "https://disify.com/api/email/%s"
MAIL_PATTERN = re.compile(r"^\w+@\w+\.\w+$")

class ResPartner(models.Model):
    _inherit = "res.partner"

    email_format_error = fields.Char("Format Validation Error", readonly=True)
    email_disposable_error = fields.Char("Disposable Validation Error", readonly=True)

    @api.onchange("email")
    def _compute_email_format_error(self):
        for record in self:
            if not record.email:
                record.email_format_error = False
                continue
            if not re.match(MAIL_PATTERN, record.email):
                record.email_format_error = "The email does not match the format \"email@example.com\""

    @api.model
    def _disify_check(self, email):
        try:
            result = requests.get(DISIFY_URL_PATTERN % email, timeout=TIMEOUT)
        except requests.exceptions.ConnectionError:
            _logger.warning("Connection Error while connection to https://disify.com")
            return False
        return result.json().get("disposable")
    
    def _check_disposable(self):
        for record in self:
            if not record.email:
                continue
            check_result = self._disify_check(record.email)
            self.env['disposable.email.check.result'].create({
                "name": record.email,
                "partner_id": record.id,
                "is_disposable": check_result
            })
            if check_result:
                record.email_disposable_error = "The email seems to be disposable"
                record.sudo().message_post(body=f"The email \"{record.email}\" seems to be disposable")
            else:
                record.email_disposable_error = False

    def action_send_email_confirmation(self):
        confirmation = self.env['partner.email.confirmation']
        for record in self.filtered("email"):
            confirmation.create({
                "name": record.email,
                "partner_id": record.id
            })

            
    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        records._check_disposable()
        return records
    
    def write(self, vals):
        result = super().write(vals)
        if "email" in vals:
            self._check_disposable()
        return result