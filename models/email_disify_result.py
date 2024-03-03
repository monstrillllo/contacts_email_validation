from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class DisposableEmaileCheckResult(models.Model):
    _name = "disposable.email.check.result"
    _description = "Results of checking emails for disposable"

    name = fields.Char("Email")
    partner_id = fields.Many2one("res.partner", "Partner")
    is_disposable = fields.Boolean(default=False, string="Is Disposable")