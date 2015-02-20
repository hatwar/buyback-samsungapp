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
					"name": "Purchase Receipt",
					"description": _("Goods received from Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Redemption Form",
					"icon": "icon-sitemap",
					"label": _("Voucher Redemption Form"),
					"description": _("Redemption Form."),
				},
				{
					"type": "doctype",
					"name": "Pin Expiry Details",
					"icon": "icon-sitemap",
					"label": _("Pin Expiry Details"),
					"description": _("Pin Expiry Details"),
				},
				{
					"type": "doctype",
					"name": "Deduction Percentage Criteria",
					"icon": "icon-sitemap",
					"label": _("Deduction Percentage Criteria"),
					"description": _("Configuration Page"),
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
				},]},
				{
			"label": _("Main Report"),
			"icon": "icon-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"label": _("Voucher Redemption Report"),
					"name": "Voucher Redeemption Report",
					"doctype": "Item"
				},]}
		
	]
