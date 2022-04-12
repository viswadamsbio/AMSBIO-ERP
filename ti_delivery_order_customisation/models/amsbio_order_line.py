# -*-coding: utf-8 -*-

from odoo import models, fields

class AmsbioOrderLine(models.Model):
    _name ="amsbio.order.line"
    _description = "Sale Order Line Details"

    # Order line fields/values 
    product_description = fields.Char("Description")
    quantity = fields.Float()
    price_unit = fields.Float("Unit Price")
    price_subtotal = fields.Float("Subtotal")