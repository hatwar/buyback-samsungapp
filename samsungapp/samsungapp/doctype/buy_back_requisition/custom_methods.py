
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months,add_days,cint,nowdate,formatdate
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc




@frappe.whitelist()
def generate_pin(PR, method):
	import string
	import random
	voucher_info=frappe.db.sql("""select voucher_type,voucher_serial_number,voucher_expiry_date from `tabBuy Back Requisition` where name='%s' and voucher_type='Paper Voucher' """%(PR.buy_back_requisition_ref),as_dict=1)
	if voucher_info:
		frappe.db.sql("update `tabPurchase Receipt` set pin='%s' where name='%s'"%(voucher_info[0]['voucher_serial_number'],PR.name))
		frappe.db.sql("update `tabPurchase Receipt` set pin_expiry='%s' where name='%s'"%(voucher_info[0]['voucher_expiry_date'],PR.name))
		create_redemption_form(PR,voucher_info[0]['voucher_serial_number'],voucher_info[0]['voucher_expiry_date'])
	else:
		code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
		frappe.db.sql("update `tabPurchase Receipt` set pin='%s' where name='%s'"%(code,PR.name))
		send_email(PR, method,code)
		send_pin_sms(PR, method,code)

def create_redemption_form(PR,pin,pin_expiry):
	# frappe.errprint(PR.pin_expiry)
	customer_details=frappe.db.sql("""select customer,id_type,id_no,offered_price,customer_image,item_code,colour from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_dict=1)
	po = frappe.new_doc('Paper Voucher Redemption Form')
	po.enter_pin=pin
	po.customer= customer_details[0]['customer']
	po.customer_image='<table style="width: 100%; table-layout: fixed;"><tr><td style="width:110px"><img src="'+cstr(customer_details[0]['customer_image'])+'" width="100px"></td></tr></table>'
	po.id_type=customer_details[0]['id_type']
	po.id_number=customer_details[0]['id_no']
	po.discount_amount=customer_details[0]['offered_price']
	po.expiry_date=pin_expiry
	po.item_code=customer_details[0]['item_code']
	po.colour=customer_details[0]['colour']
	# po.warehouse = user_permissions['Warehouse'][0]
	po.save()
	msgprint(_("{0} is Created Successfully.").format(po.name))
	# frappe.errprint("Done")

def send_email(PR, method,code):
	recipients=[]
	expiry_date=''
	cust=''
	customer=frappe.db.sql("""select email_id ,customer from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_list=1)
	if customer:
		recipients.append(cstr(customer[0][0]))
		cust=cstr(customer[0][1])
	no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1)
	if no_of_days:
		expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
		if expiry_date:
			frappe.db.sql("update `tabPurchase Receipt` set pin_expiry='%s' where name='%s'"%(expiry_date,PR.name))
	if recipients:
		subject = "Voucher Generation"
		message ="""<h3>Dear   %s</h3><p>The  PIN  below  is  generated against your transaction   %s at    '%s' </p>
		<p>PIN:     %s</p>
		<p>PIN Expiry Date:    %s </p>
		<p>Kindly redeem the  voucher  before  the  expiry  date.</p>
		<p>Thank You,</p>
		""" %(cust,PR.buy_back_requisition_ref,PR.warehouse,code,formatdate(expiry_date))
		frappe.sendmail(recipients, subject=subject, message=message)	




def send_pin_sms(PR, method,code):
	recipients=[]
	expiry_date=''
	customer=frappe.db.sql("""select phone_no ,customer from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_list=1)
	if customer:
		recipients.append(cstr(customer[0][0]))
		cust=cstr(customer[0][1])
	no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1)
	if no_of_days:
		expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
	if recipients:
		message ="""Dear %s,\nThe PIN below is generated against your transaction %s at '%s',\nPIN: %s,\nPIN Expiry Date: %s,\nKindly redeem the  voucher  before  the  expiry  date.\nThanks You.""" %(cust,PR.buy_back_requisition_ref,PR.warehouse,code,formatdate(expiry_date))
		send_sms(recipients,cstr(message))





def set_missing_values(source, target):
	target.ignore_pricing_rule = 1
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")

@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	return new_purchase_receipt(source_name,target_doc=None)
	
def new_purchase_receipt(source_name,target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.conversion_factor)
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (flt(obj.qty) - flt(obj.received_qty)) * \
			flt(obj.rate) * flt(source_parent.conversion_rate)

	doc = get_mapped_doc("Purchase Order", source_name,	{
		"Purchase Order": {
			"doctype": "Purchase Receipt",
			"field_map": {
				# "warehouse": "warehouse",
			},
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Receipt Item",
			"field_map": {
				"name": "prevdoc_detail_docname",
				"parent": "prevdoc_docname",
				"parenttype": "prevdoc_doctype",
				"serial_no":"serial_no",
			},
			"postprocess": update_item,
			"condition": lambda doc: doc.received_qty < doc.qty
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)
	pr = doc.save()
	doc.submit()
	msgprint(_("{0} is Created Successfully.").format(doc.name))

	return doc




