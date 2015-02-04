
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.email_lib import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months,add_days,cint,nowdate,formatdate
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms



@frappe.whitelist()
def generate_pin(PR, method):
	import string
	import random
	code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	frappe.db.sql("update `tabPurchase Receipt` set pin='%s' where name='%s'"%(code,PR.name))
	frappe.errprint("code")
	send_email(PR, method,code)
	send_pin_sms(PR, method,code)



def send_email(PR, method,code):
	recipients=[]
	expiry_date=''
	cust=''
	customer=frappe.db.sql("""select email_id ,customer from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_list=1,debug=1)
	if customer:
		recipients.append(cstr(customer[0][0]))
		cust=cstr(customer[0][1])
	no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1,debug=1)
	if no_of_days:
		expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
	if recipients:
		subject = "Voucher Generation"
		message ="""<h3>Dear %s</h3><p>Below PIN is generated against the device sold at Matrix store </p>
		<p>PIN:%s</p>
		<p>PIN Expiry Date:%s </p>
		<p>Kindly redeem the voucher before the expiry date.</p>
		<p>Thank You,</p>
		""" %(cust,code,formatdate(expiry_date))
		sendmail(recipients, subject=subject, msg=message)	




def send_pin_sms(PR, method,code):
	recipients=[]
	customer=frappe.db.sql("""select phone_no ,customer from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_list=1,debug=1)
	if customer:
		recipients.append(cstr(customer[0][0]))
		cust=cstr(customer[0][1])
	no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1,debug=1)
	if no_of_days:
		expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
	if recipients:
		message ="""Dear %s
		Below PIN is generated against the device sold at Matrix store
		PIN:%s
		PIN Expiry Date:%s 
		Kindly redeem the voucher before the expiry date.
		Thank You.""" %(cust,code,formatdate(expiry_date))
		send_sms(recipients,cstr(message))










