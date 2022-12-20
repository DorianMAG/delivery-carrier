# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PackageType(models.Model):
    _inherit = "stock.package.type"

    is_strict_weight = fields.Boolean(
        string="Overweight forbidden",
        help="The maximum weight of the package can't be exceeded.",
        compute="_compute_is_strict_weight",
        store=True,
        readonly=False,
    )

    @api.depends("package_carrier_type")
    def _compute_is_strict_weight(self):
        for rec in self:
            carrier_id = self.env["delivery.carrier"].search(
                [("delivery_type", "=", rec.package_carrier_type)], limit=1
            )
            rec.is_strict_weight = (
                rec.carrier_id.delivery_carrier_strict_weight_package
                if carrier_id
                else False
            )
