





cur_frm.cscript.enter_pin = function(doc, cdt, cdn){
	console.log("in the image");
	console.log(doc.enter_pin);

	return  frappe.call({
		method: 'samsungapp.samsungapp.doctype.slot_cashier.slot_cashier.check_pin',
		args: {
			pin: doc.enter_pin
		},
		callback: function(r) {
			console.log(r.message)
				doc.id_type =r.message[0]['id_type'];
				doc.id_number=r.message[0]['id_no'];
				doc.customer=r.message[0]['customer']
				doc.discount_amount=r.message[0]['offered_price']
				doc.expiry_date=r.message[0]['expiry_date']
				refresh_field('id_type');
				refresh_field('id_number');
				refresh_field('customer');
				refresh_field('expiry_date')
				refresh_field('discount_amount')
		}
	});

}
