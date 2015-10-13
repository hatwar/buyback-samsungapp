# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months,formatdate,cstr,flt,fmt_money
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms
from frappe import msgprint, _


class BuyBackRequisition(Document):

	def validate(self):
		self.is_serial_no_added()
		self.check_imei(self.iemi_number)
		self.check_basic_price()
		self.check_paper_voucher()
		self.serial_no_paper_voucher()

	def is_serial_no_added(self):
		is_required = frappe.db.get_value("Item", self.item_code, "has_serial_no")
		if is_required == 'No':
			frappe.throw(_("Item {0} is not setup for Serial Nos. Check Item master").format(self.item_code))
	

	def serial_no_paper_voucher(self):
		if self.voucher_type=='Paper Voucher':
			check_exist=frappe.db.sql("""select name, voucher_serial_number from `tabBuy Back Requisition` where voucher_serial_number='%s' and docstatus=1"""%(self.voucher_serial_number),as_list=1)
			if check_exist:
				msgprint(_("Voucher Serial Number is already exist!"),raise_exception=1)




	def check_paper_voucher(self):
		# frappe.errprint("in the check_paper_voucher")
		if self.voucher_type=='Paper Voucher':
			if not( self.voucher_serial_number and self.voucher_expiry_date):
				msgprint(_("Please Enter Serial Number and Expiry Date For Paper Voucher!"),raise_exception=1)
			

	def check_basic_price(self):
		if not self.basic_price:
			msgprint(_("Please Set The Basic Item Price!"),raise_exception=1)

			
	def get_warehouse(self):
		user_permissions = frappe.defaults.get_user_permissions(frappe.session.user)
		if user_permissions.has_key('Warehouse'):
			return{
			"warehouse":user_permissions['Warehouse'][0]
			}


	def check_imei(self,iemi_number):
		exist_imei=frappe.db.sql("""select iemi_number,name from `tabBuy Back Requisition` where iemi_number='%s' and docstatus = 1
					"""%(iemi_number),as_dict=1)
		if exist_imei:
			msgprint(_("IMEI Number is already exist!"),raise_exception=1)


@frappe.whitelist()
def get_basic_price(item_code,price_list):
	basic_price=frappe.db.sql("""select price_list_rate from `tabItem Price` where item_code='%s'
					and price_list='%s' """%(item_code,price_list),as_dict=1)
	if basic_price:
		return [{
					"basic_price": basic_price[0]['price_list_rate'],
				}]
	else:
		msgprint(_("Please Set The Basic Item Price"), raise_exception=1)
						


@frappe.whitelist()
def save(BuyBackRequisition, method):
	user_permissions = frappe.defaults.get_user_permissions(frappe.session.user)
	if user_permissions.has_key('Warehouse'):
		if BuyBackRequisition.customer_acceptance=='Yes':
			po = frappe.new_doc('Purchase Order')
			if BuyBackRequisition.voucher_type=='Paper Voucher':
				po.paper_voucher_pin=BuyBackRequisition.voucher_serial_number
			po.supplier= 'Slot buy back program'
			po.naming_series="PO-BB-"
			po.buy_back_requisition_ref=BuyBackRequisition.name
			po.colour=BuyBackRequisition.colour
			po.imei_number=BuyBackRequisition.iemi_number
			po.warehouse=user_permissions['Warehouse'][0]
			poc = po.append('items', {})
			poc.item_code=BuyBackRequisition.item_code
			poc.schedule_date=nowdate()
			poc.rate=BuyBackRequisition.offered_price
			poc.serial_no=BuyBackRequisition.iemi_number
			poc.warehouse=user_permissions['Warehouse'][0]
			po.save()
			po.submit()
			msgprint(_("{0} is Created Successfully.").format(po.name))
			send_device_recv_email(BuyBackRequisition, method)
	else:
		msgprint(_("Please set the Warehouse in User Permissions !"), raise_exception=1)	


@frappe.whitelist()
def get_device_active_Details(active):
	active_percentage=[]
	if active=='Yes':
		active_percentage=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
					and field='device_active_yes_percentage' """)
	elif active=='No':
		active_percentage=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
					and field='device_active_no_percentage' """)
	else:
		pass

	if len(active_percentage) >0:
		return active_percentage[0][0]
	else:

		return 0

@frappe.whitelist()
def get_functional_defects_details(functional_defects,active):
	functional_value=[]
	if active=='Yes':
		if functional_defects=='Yes':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='active_yes_percentage' """)
		elif functional_defects=='No':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='active_no_percentage' """)
			# frappe.errprint(functional_value)	
		else:
			pass

	elif active=='No':
		if functional_defects=='Yes':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactivate_yes_percentage' """)
		elif functional_defects=='No':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactivate_no_percentage' """)
		else:
			pass
			

	if len(functional_value)>0:
		return functional_value[0][0]
	else:
		return 0

@frappe.whitelist()
def get_condition_of_screen(screen_condition,active):
	# frappe.errprint(screen_condition)
	screen=[]
	if active=='Yes':
		# frappe.errprint("in active yes")
		if screen_condition=='Broken Screen':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_broken_screen' """)
		elif screen_condition=='Poor':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_poor_screen' """)
		elif screen_condition=='Just OK':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_just_ok_screen' """)
		elif screen_condition=='Excellent':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_excellent_screen' """)
	elif active=='No':
		if screen_condition=='Broken Screen':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_broken_screen' """)
		elif screen_condition=='Poor':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_poor_screen' """)
		elif screen_condition=='Just OK':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_just_ok_screen' """)
		elif screen_condition=='Excellent':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_excellent_screen' """)
	else:
		pass

	if len(screen)>0:
		return screen[0][0]
	else:
		return 0

@frappe.whitelist()
def get_condition_of_device_body(device_body,active):
	body_condition=[]
	if active=='Yes':
		if device_body=='Poor':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_poor_body_condition' """)
		elif device_body=='Just OK':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='just_ok_body' """)
		elif device_body=='Excellent':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='excellent_body' """)
	elif active=='No':
		if device_body=='Poor':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_poor_body' """)
		elif device_body=='Just OK':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_just_ok_body' """)
		elif device_body=='Excellent':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_excellent' """)
	else:
		pass

	if len(body_condition)>0:
		return body_condition[0][0]
	else:
		return 0


@frappe.whitelist()
def get_accessories_details(accessories,active):
	accessories_details=[]
	if active=='Yes':
		if accessories=='Yes':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='accessories_yes_percentage' """)
		elif accessories=='No':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='accessories_no_percentage' """)

	elif active=='No':
		if accessories=='Yes':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_yes_accessories' """)
		elif accessories=='No':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_no_accessories' """)

	else:
		pass

	if len(accessories_details)>0:
		return accessories_details[0][0]
	else:
		return 0


# code done by Tejal for algorithm

@frappe.whitelist()
def get_capacity(capacity,active):
	capacity_details=[]
	if active=='Yes':
		if capacity=='8GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_percentage' """)
			# frappe.errprint(capacity_details)
		elif capacity=='16GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_one_percentage' """)
		elif capacity=='32GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_two_percentage' """)
		elif capacity=='64GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_tr_percentage' """)
		elif capacity=='128GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_fr_percentage' """)
		elif capacity=='N/A':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='not_applicable_percentage' """)
	elif active=='No':
		if capacity=='8GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_8gb' """)
		elif capacity=='16GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_16gb' """)
		elif capacity=='32GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_32gb' """)
		elif capacity=='64GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_64gb' """)
		elif capacity=='128GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_128gb' """)
		elif capacity=='N/A':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_na' """)
	if len(capacity_details)>0:
		return capacity_details[0][0]
	else:
		return 0


# @frappe.whitelist()
def send_device_recv_email(BuyBackRequisition, method):
	recipients=[]
	expiry_date=''
	if BuyBackRequisition.email_id:
		recipients.append(BuyBackRequisition.email_id)
	recipient=frappe.db.sql("""select parent from `tabDefaultValue` where 
								defkey='Warehouse' and defvalue='%s' 
								and  parent in (select parent from `tabUserRole` 
								where role in('MPO','Collection Officer','Redemption Officer'))"""%BuyBackRequisition.warehouse,as_dict=1)
	if recipient:
		for resp in recipient:
			recipients.append(resp['parent'])
	if recipients:
		subject = "Device Received"
		message ="""<h3>Dear  %s</h3><p> We received your device at    '%s', below are the details</p>
		<p>Transaction ID:   %s</p>
		<p>Device Received:   %s</p>
		<p>Received Date:     %s </p>
		<p>Offered Price:    %s</p>
		<p>Your voucher will be sent to you in a separate email & sms correspondence.</p>
		<p>Thank You,</p>
		""" %(BuyBackRequisition.customer,BuyBackRequisition.warehouse,BuyBackRequisition.name,BuyBackRequisition.item_name,formatdate(BuyBackRequisition.creation),fmt_money(flt(BuyBackRequisition.offered_price)))
		frappe.sendmail(recipients, subject=subject, message=message)


def send_to_sms(BuyBackRequisition, method):
	recipients=[]
	if BuyBackRequisition.phone_no:
		phone_no=BuyBackRequisition.phone_no
		recipients.append(cstr(phone_no))
		message ="""Dear %s , We received your device at    '%s', 
					below are the details
					Transaction ID:		%s,
					Device Received:	%s,
					Received Date:		%s,
					Offered Price:		%s,
					Your voucher will be sent to you in a separate email & sms correspondence.
			Thank You.""" %(BuyBackRequisition.customer,BuyBackRequisition.warehouse,BuyBackRequisition.name,BuyBackRequisition.item_name,formatdate(BuyBackRequisition.creation),fmt_money(flt(BuyBackRequisition.offered_price)))
		send_sms(recipients,cstr(message))












