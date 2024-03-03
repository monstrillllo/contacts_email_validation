from odoo import _, api, fields, models
import datetime
import secrets

CONFIRMATION_LIFE_TIME = datetime.timedelta(hours=1)

class EmailConfirmation(models.Model):
    _name = "partner.email.confirmation"
    _description = "Partner Email Confirmation"

    name = fields.Char(string="email", required=True)
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    state = fields.Selection([
        ['pending', 'Pending'],
        ['expired', 'Expired'],
        ['confirmed', 'Confirmed']
        ], required=True, default="pending")
    confirmation_token = fields.Char("Confirmation Token", required=True, readonly=True, default=lambda self: secrets.token_urlsafe(32))
    confirmation_url = fields.Char("Confirmation URL", compute="_compute_url")

    @api.depends("confirmation_token")
    def _compute_url(self):
        for record in self:
            record.confirmation_url = "/email/%s/%s" % (record.name, record.confirmation_token)

    @api.model
    def _update_confirmation_states(self):
        pending = self.search([['state', '=', 'pending']])
        now = fields.Datetime.now()
        pending.filtered(lambda c: now >= c.create_date + CONFIRMATION_LIFE_TIME).write({'state': 'expired'})
    
    def _confirm_email(self):
        for record in self.sudo():
            record.write({"state": "confirmed"})
            record.partner_id.message_post(body=f"The email \"{record.name}\" was confirmed!", message_type='comment', author_id=record.create_uid.partner_id.id)

    def _send_confirmation_email(self):
        for record in self:
            template_id = self.env.ref('contacts_email_validation.email_confirmation_email_template')
            template_id.send_mail(record.id, force_send=True)

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            pending_confirmations = self.search([['id', '!=', record.id], ['name', '=', record.name], ['partner_id', '=', record.partner_id.id], ['state', '=', 'pending']])
            if pending_confirmations:
                pending_confirmations.state = "expired"
        records._send_confirmation_email()
