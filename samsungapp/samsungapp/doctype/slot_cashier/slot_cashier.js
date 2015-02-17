cur_frm.cscript.enter_pin = function(doc, cdt, cdn){
	return cur_frm.call({
			doc: cur_frm.doc,
			method: "check_pin",
			args: doc.enter_pin,
			callback: function(r) {
				if(r.message['ret']=='ret') {
					cur_frm.set_value("enter_pin", null)
					refresh_field('enter_pin')
				}
				console.log(r.message)
				cur_frm.set_value("customer", r.message['customer'])
				cur_frm.set_value("id_type", r.message['id_type'])
				cur_frm.set_value("id_number", r.message['id_no'])
				cur_frm.set_value("discount_amount", r.message['offered_price'])
				cur_frm.set_value("expiry_date", r.message['expiry_date'])
				cur_frm.set_value("colour", r.message['colour'])
				cur_frm.set_value("item_code", r.message['item_code'])
				cur_frm.set_value("customer_image",'<table style="width: 100%; table-layout: fixed;"><tr><td style="width:110px"><img src="'+r.message['customer_image']+'" width="100px"></td></tr></table>')

				
	
				refresh_field('id_type');
				refresh_field('id_number');
				refresh_field('customer');
				refresh_field('expiry_date');
				refresh_field('discount_amount');
				refresh_field('customer_image');
				refresh_field('item_code');
				refresh_field('colour');
				cur_frm.refresh();
				
			},
		
		})
}



cur_frm.cscript.validate= function(doc,cdt,cdn){
        if(doc.enter_pin)
        {
		cur_frm.cscript.enter_pin(doc,cdt,cdn);	
	    }
		if (doc.iemi_no)
		{
        cur_frm.cscript.iemi_no(doc,cdt,cdn);
        }

       
		}


cur_frm.cscript.iemi_no = function(doc,cdt,cdn){
		var value = Math.floor(doc.iemi_no);
		if (Math.floor(doc.iemi_no) == value) {
			if (! /^[0-9]{15}$/.test(doc.iemi_no)) {
			  msgprint("IMEI should have 15 digits!!");
			  throw "Please Enter exactly 15 digits!"
			  return false;
			}
			} else {
			  cur_frm.set_value("iemi_no", '')
			  msgprint("IEMI Requires Numeric Values ");
			  throw "Please Enter exactly 15 digits!"
			}

	}




