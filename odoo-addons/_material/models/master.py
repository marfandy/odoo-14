from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = "master.material"
    _description = "Master Materials"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    type = fields.Selection(
        [("fabric", "Fabric"), ("jeans", "Jeans"), ("cotton", "Cotton")],
        string="Type",
        required=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    buy_price = fields.Monetary(
        string="Buy Price", currency_field="currency_id", required=True
    )
    supplier_id = fields.Many2one("master.supplier", string="Supplier", required=True)

    @api.constrains("buy_price")
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(
                    "Buy Price should be greater than or equal to 100."
                )


class Supplier(models.Model):
    _name = "master.supplier"
    _description = "Suplliers"

    name = fields.Char(string="Name", required=True)
