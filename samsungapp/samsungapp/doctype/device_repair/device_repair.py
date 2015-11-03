# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DeviceRepair(Document):
	pass


@frappe.whitelist()
def get_customer(sales_order):
	customer=frappe.db.get_value("Sales Order",sales_order,"customer")
	repair_parts=frappe.db.sql("""select * from `tabSales Order Item` where parent='%s'"""%(sales_order),as_dict=1)
	return customer,repair_parts

@frappe.whitelist()
def get_item(purchase_receipt):
	item_code=frappe.db.get_value("Purchase Receipt Item",{'parent':purchase_receipt},"item_code")
	frappe.errprint(item_code)
	return item_code