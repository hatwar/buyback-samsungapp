from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Buy Back Requisition",
					"icon": "icon-sitemap",
					"label": _("Buy Back Requisition Form"),
					"description": _("Buy Back Requisition Form"),
				},
				{
					"type": "doctype",
					"name": "Purchase Order",
					"description": _("Purchase Orders given to Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Slot Cashier",
					"icon": "icon-sitemap",
					"label": _("Voucher Redeemption Form"),
					"description": _("Slot Cashier."),
				},
				{
					"type": "doctype",
					"name": "Id Type",
					"icon": "icon-sitemap",
					"label": _("Id Type"),
					"description": _("Id Type"),
				},
				{
					"type": "doctype",
					"name": "Pin Expiry Details",
					"icon": "icon-sitemap",
					"label": _("Pin Expiry Details"),
					"description": _("Pin Expiry Details"),
				}
			]
		},
		{
			"label": _("Main Report"),
			"icon": "icon-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Buy Back Report",
					"doctype": "Item"
				},]}
		
	]
