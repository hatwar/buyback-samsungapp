
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.email_lib import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months



@frappe.whitelist()
def generate_pin(PR, method):
	frappe.errprint("in the generate pin")
	import string
	import random
	code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	PR.pin=code
	frappe.errprint(code)



def send_email(PR, method):
	frappe.errprint("in the send email")
	customer=frappe.db.sql("""select customer from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_dict=1,debug=1)
	frappe.errprint(customer)
	recipients=frappe.db.sql("""select parent from `tabUserRole` where role in('MSE','Slot Cashier','Slot Representative')""")
	frappe.errprint(recipients)
	# recipients = frappe.db.get_value("", None, "send_notifications_to").split(",")






