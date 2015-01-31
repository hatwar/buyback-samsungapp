# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months

class BuyBackRequisition(Document):
	pass



@frappe.whitelist()
def test(BuyBackRequisition, method):
	frappe.errprint("BuyBackRequisition.name")
	frappe.errprint(BuyBackRequisition.customer_acceptance)


@frappe.whitelist()
def save(BuyBackRequisition, method):
	frappe.errprint("in the save")
	frappe.errprint(BuyBackRequisition.customer_acceptance)
	if BuyBackRequisition.customer_acceptance=='Yes':
		po = frappe.new_doc('Purchase Order')
		po.supplier= 'Slot buy back program'
		po.naming_series="PO-BB-"
		po.buy_back_requisition_ref=BuyBackRequisition.name
		poc = po.append('po_details', {})
		poc.item_code=BuyBackRequisition.item_code
		poc.schedule_date=nowdate()
		poc.rate=BuyBackRequisition.offered_price
		po.insert(ignore_permissions=True)