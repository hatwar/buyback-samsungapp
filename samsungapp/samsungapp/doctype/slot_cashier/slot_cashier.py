# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint
from frappe.utils import today,add_days,cint,nowdate,formatdate,cstr
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms


class SlotCashier(Document):
	pass



@frappe.whitelist()
def check_pin(pin):
	frappe.errprint("in the check_pin pin")
	slot_cashier=frappe.db.sql("""select name from `tabSlot Cashier` where enter_pin='%s' """%(pin),as_dict=1,debug=1)
	if slot_cashier:
		msgprint("Already Reedemed",raise_exception=1)
	else:
		buy_back_requisition_ref=frappe.db.sql("""select buy_back_requisition_ref,creation from `tabPurchase Receipt` where pin='%s' """%(pin),as_dict=1,debug=1)
		no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1,debug=1)
		frappe.errprint(no_of_days)
		if no_of_days:
			expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
		else:
			expiry_date=" "
		if buy_back_requisition_ref:
			customer_details=frappe.db.sql("""select customer,id_type,id_no,offered_price from `tabBuy Back Requisition` where name='%s' """%(buy_back_requisition_ref[0]['buy_back_requisition_ref']),as_dict=1,debug=1)
			if customer_details:
				return [{
					"customer": customer_details[0]['customer'],
					"id_type":customer_details[0]['id_type'],
					"id_no":customer_details[0]['id_no'],
					"offered_price":customer_details[0]['offered_price'],
					"expiry_date":cstr(expiry_date)
					
				}]	


@frappe.whitelist()
def send_reedemed_email(Voucher, method):
	from frappe.utils.email_lib import sendmail
	frappe.errprint("inth send_reedemed_email")
	recipients=[]
	expiry_date=''
	if Voucher.customer:
		customer=frappe.db.sql("""select email_id from `tabCustomer` where name='%s' """%(Voucher.customer),as_list=1,debug=1)
		if customer:
			recipients.append(customer[0][0])	
	recipient=frappe.db.sql("""select parent from `tabUserRole` where role in('MSE','Slot Cashier','Slot Representative')""",as_dict=1,debug=1)
	if recipient:
		for resp in recipient:
			recipients.append(resp['parent'])
	frappe.errprint(recipients)		
	if recipients:
		subject = "Device Received"
		message ="""<h3>Dear %s </h3><p>Your voucher is redeemed against the PIN </p>
		<p>Value of the voucher :%s</p>
		<p>Redemption Date:%s </p>
		<p>Thank You,</p>
		""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		sendmail(recipients, subject=subject, msg=message)	



@frappe.whitelist()
def send_redeemed_sms(Voucher, method):
	recipients=[]
	if Voucher.customer:
		customer=frappe.db.sql("""select phone_no from `tabCustomer` where name='%s' """%(Voucher.customer),as_list=1,debug=1)
		if customer:
			recipients.append(customer[0][0])	
	frappe.errprint(recipients)		
	if recipients:
		message ="""Dear %s
		Your voucher is redeemed against the PIN.
		Value of the voucher :%s
		Redemption Date:%s 
		Thank You.""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		send_sms(recipients,cstr(message))	





