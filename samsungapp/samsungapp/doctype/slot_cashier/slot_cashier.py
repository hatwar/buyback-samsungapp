# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
from frappe.utils import today,add_days,cint,nowdate,formatdate,cstr,getdate
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms
import frappe
from frappe import msgprint, _


class SlotCashier(Document):

	def validate(self):
		self.exist_pin(self.enter_pin)



	def check_pin(self,pin):
		buy_back_requisition_ref=frappe.db.sql("""select buy_back_requisition_ref,creation from `tabPurchase Receipt` where pin='%s' """%(pin),as_dict=1)
		no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1,debug=1)
		if no_of_days:
			expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
		else:
			expiry_date=""
		if buy_back_requisition_ref:
			customer_details=frappe.db.sql("""select customer,id_type,id_no,offered_price,customer_image,item_code,colour from `tabBuy Back Requisition` where name='%s' """%(buy_back_requisition_ref[0]['buy_back_requisition_ref']),as_dict=1)
			if customer_details:
				return {
					"customer": customer_details[0]['customer'],
					"id_type":customer_details[0]['id_type'],
					"id_no":customer_details[0]['id_no'],
					"offered_price":customer_details[0]['offered_price'],
					"expiry_date":cstr(expiry_date),
					"customer_image":customer_details[0]['customer_image'],
					"item_code":customer_details[0]['item_code'],
					"colour":customer_details[0]['colour']
					
				}
		

	def exist_pin(self,pin):
		# frappe.errprint("in the exist pin")
		buy_back_requisition_ref=frappe.db.sql("""select buy_back_requisition_ref,creation from `tabPurchase Receipt` where pin='%s' """%(pin),as_dict=1)
		if not buy_back_requisition_ref:
			slot_cashier=frappe.db.sql("""select name,mark_voucher_as_redeemed,expiry_date from `tabSlot Cashier` where enter_pin='%s'"""%(pin),as_dict=1)
			if not slot_cashier:
				msgprint(_("Voucher is Invalid!"),raise_exception=1)
			elif slot_cashier[0]['mark_voucher_as_redeemed']==1 :
				msgprint(_("Voucher is already reedemed!"),raise_exception=1)
			elif getdate(slot_cashier[0]['expiry_date'])<getdate(nowdate()):
				msgprint(_("Voucher is Expired!"),raise_exception=1)
			else:
				pass
				

						


@frappe.whitelist()
def send_reedemed_email(Voucher, method):
	from frappe.utils.email_lib import sendmail
	recipients=[]
	expiry_date=''
	if Voucher.customer:
		customer=frappe.db.sql("""select email_id from `tabCustomer` where name='%s' """%(Voucher.customer),as_list=1)
		if customer:
			recipients.append(customer[0][0])	
	recipient=frappe.db.sql("""select parent from `tabUserRole` where role in('MPO','Collection Officer','Redemption Officer')""",as_dict=1,debug=1)
	if recipient:
		for resp in recipient:
			recipients.append(resp['parent'])
	if recipients:
		subject = "Voucher Redemption"
		if Voucher.mark_voucher_as_redeemed==1:
			message ="""<h3>Dear %s </h3><p>Your voucher is redeemed against the PIN </p>
			<p>Value of the voucher :%s</p>
			<p>Redemption Date:%s </p>
			<p>Thank You,</p>
			""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		else:  
			message ="""<h3>Dear %s </h3><p>Your voucher is not redeemed against the PIN </p>
			<p>Value of the voucher :%s</p>
			<p>Date:%s </p>
			<p>Thank You,</p>
			""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		sendmail(recipients, subject=subject, msg=message)	



@frappe.whitelist()
def send_redeemed_sms(Voucher, method):
	recipients=[]
	if Voucher.customer:
		customer=frappe.db.sql("""select phone_no from `tabCustomer` where name='%s' """%(Voucher.customer),as_list=1)
		if customer:
			recipients.append(customer[0][0])	
	if recipients:
		if Voucher.mark_voucher_as_redeemed==1:
			message ="""Dear %s
			Your voucher is redeemed against the PIN
			Value of the voucher :%s
			Redemption Date:%s 
			Thank You.
			""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		else:
			message ="""Dear %s
			Your voucher is but not redeemed against the PIN 
			Value of the voucher :%s
			Date:%s 
			Thank You.
			""" %(Voucher.customer,Voucher.discount_amount,formatdate(Voucher.creation))
		send_sms(recipients,cstr(message))	





