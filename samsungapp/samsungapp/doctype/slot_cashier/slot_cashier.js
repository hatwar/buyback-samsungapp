cur_frm.cscript.enter_pin = function(doc, cdt, cdn){
	return cur_frm.call({
			doc: cur_frm.doc,
			method: "check_pin",
			args: doc.enter_pin,
			callback: function(r) {
				if(r.message['ret']=='ret') {
					cur_frm.set_value("enter_pin", '')
					refresh_field('enter_pin')
				}
				cur_frm.set_value("customer", r.message['customer'])
				cur_frm.set_value("id_type", r.message['id_type'])
				cur_frm.set_value("id_number", r.message['id_no'])
				cur_frm.set_value("discount_amount", r.message['offered_price'])
				cur_frm.set_value("expiry_date", r.message['expiry_date'])

				refresh_field('id_type');
				refresh_field('id_number');
				refresh_field('customer');
				refresh_field('expiry_date');
				refresh_field('discount_amount');
				cur_frm.refresh();
				
			},
		
		})
}

cur_frm.cscript.iemi_no = function(doc,cdt,cdn){
		var value = Math.floor(doc.iemi_no);
		if (Math.floor(doc.iemi_no) == value) {
			if (! /^[0-9]{15}$/.test(doc.iemi_no)) {
			  msgprint("Please Enter  exactly 15 digits!");
			  return false;
			}
			} else {
			  msgprint("IEMI Requires Numeric Values ");
			}

	}




