# -*-coding: utf-8 -*-

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_id = fields.Many2one(states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]}, domain="[('type', '=', 'contact'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")