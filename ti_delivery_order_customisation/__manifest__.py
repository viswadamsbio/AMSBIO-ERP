# -*-coding: utf-8 -*-
{
    'name'          : "TI Delivery Order Customisation",
    'author'        : "Target Integration",
    'summary'       : "Display sale order lines in delivery orders",
    'version'       : "14.0.0.0",
    'website'       : "http://www.targetintegration.com",
    'category'      : "Inventory/Inventory",
    'depends'       : [
                        "ti_warehouse_count"
                    ],
    'data'          : [
                        "security/ir.model.access.csv",
                        "views/stock_picking_views.xml"
                    ]
}