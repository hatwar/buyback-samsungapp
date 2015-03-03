# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PaperVoucherRedemptionForm(Document):
	def get_warehouse(self):
		user_permissions = frappe.defaults.get_user_permissions(frappe.session.user)
		if user_permissions.has_key('Warehouse'):
			return{
			"warehouse":user_permissions['Warehouse'][0]
			}	
