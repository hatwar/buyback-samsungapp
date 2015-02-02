cur_frm.add_fetch("item_code", "item_name", "item_name");
cur_frm.add_fetch("customer", "customer_name", "customer_name");
cur_frm.add_fetch("customer", "email_id", "email_id");
cur_frm.add_fetch("customer", "phone_no", "phone_no");

cur_frm.add_fetch("item_code", "basic_price", "basic_price");

cur_frm.cscript.basic_price = function(doc,cdt,cdn){
	//console.log("in basic price")
	doc.estimated_price=doc.basic_price
	doc.offered_price=doc.basic_price
	refresh_field('estimated_price');
	refresh_field('device_active');
	refresh_field('offered_price');
}

cur_frm.cscript.is_the_device_active = function(doc,cdt,cdn){
	//console.log(doc.is_the_device_active)
	 frappe.call({
                method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_device_active_Details",
                args:{"active":doc.is_the_device_active},
                callback:function(r){
                        console.log(r.message)
                        console.log(doc.is_the_device_active)
                        if(doc.is_the_device_active=='Yes'){
                        	if (r.message==0){
								doc.estimated_price=doc.basic_price
								doc.offered_price=doc.basic_price
								doc.device_active=0.0
								refresh_field('device_active');
								refresh_field('offered_price')
								cur_frm.cscript.update_totals(doc);
							}
							else if (r.message>0){
								var value = r.message/100
								console.log(value)
								price=value*doc.basic_price
								doc.device_active=price
								refresh_field('device_active');
								cur_frm.cscript.update_totals(doc);
							}
						}
						else if(doc.is_the_device_active=='No'){
							if (r.message==0){
								doc.estimated_price=doc.basic_price
								doc.offered_price=doc.basic_price
								doc.device_active=0.0
								refresh_field('device_active');
								refresh_field('offered_price')
								cur_frm.cscript.update_totals(doc);
							}
							else if (r.message>0){
								var value = r.message/100
								console.log(value)
								price=value*doc.basic_price
								doc.device_active=0.0
								doc.estimated_price=price;
								doc.offered_price=price
								doc.basic_price=price
								refresh_field('device_active');
								refresh_field('estimated_price');
								refresh_field('offered_price');
								refresh_field('basic_price');
								//cur_frm.cscript.update_totals(doc);
							};
						}
                }
        })
	
}

cur_frm.cscript.does_it_have_any_functional_defects = function(doc,cdt,cdn){
	if(doc.is_the_device_active=='Yes'|| doc.is_the_device_active=='No'){

		frappe.call({
            	    method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_functional_defects_details",
            	    args:{"functional_defects":doc.does_it_have_any_functional_defects,
            				"active":doc.is_the_device_active},
            	    callback:function(r){
            	    	console.log(r.message)
						if (r.message==0){
							doc.functional_defects=0.0
							refresh_field('functional_defects');
							cur_frm.cscript.update_totals(doc);	
						}

						else if (r.message>0){
							value=r.message/100
							doc.functional_defects=value*doc.basic_price
							refresh_field('functional_defects');
							cur_frm.cscript.update_totals(doc);	

							}	
                	}
        	})
	

		}

	else{
		msgprint("Please specify device is activate or not");
	}
	
}

cur_frm.cscript.condition_of_the_screen = function(doc,cdt,cdn){
	if(doc.is_the_device_active=='Yes'|| doc.is_the_device_active=='No'){
		frappe.call({
            	    method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_condition_of_screen",
            	    args:{"screen_condition":doc.condition_of_the_screen,
            	           "active":doc.is_the_device_active},
            	    callback:function(r){
            	    	console.log(r.message)
							if(r.message==0){
								//price=(0.3*doc.basic_price)
								doc.screen_condition=0.0
								refresh_field('screen_condition')
								cur_frm.cscript.update_totals(doc);
							}
							else if (r.message>0){
								value=r.message/100
								price=(value*doc.basic_price)
								doc.screen_condition=price
								refresh_field('screen_condition')
								cur_frm.cscript.update_totals(doc);
							}

					}	

	})
}
	else{
		msgprint("Please specify device is activate or not");
	}
}

cur_frm.cscript.condition_of_device_body = function(doc,cdt,cdn){
	//console.log("in condition_of_device_body")
	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){
		frappe.call({
            	    method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_condition_of_device_body",
            	    args:{"device_body":doc.condition_of_device_body,
            	           "active":doc.is_the_device_active},
            	    callback:function(r){
						if(r.message==0){
							doc.body_condition=0.0
							refresh_field('body_condition');
							cur_frm.cscript.update_totals(doc);
						}
						else if (r.message>0){
							value=r.message/100
							doc.body_condition=value*doc.basic_price
							refresh_field('body_condition');
							cur_frm.cscript.update_totals(doc);
						}
	}

 })
}
	else{
		msgprint("Please specify device is activate or not");

	}
}

cur_frm.cscript.accessories_included = function(doc,cdt,cdn){
	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){
		frappe.call({
            	    method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_accessories_details",
            	    args:{"accessories":doc.accessories_included,
            	           "active":doc.is_the_device_active},
            	    callback:function(r){
						if (r.message==0){
							doc.accessories=0.0
							refresh_field('accessories')
							cur_frm.cscript.update_totals(doc);
						}
						else if (r.message>0){
							value=r.message/100
							doc.accessories=value*doc.basic_price
							refresh_field('accessories')
							cur_frm.cscript.update_totals(doc);
						}
					}
			})
	}
	else{
		msgprint("Please specify device is activate or not");

	}
}

cur_frm.cscript.capacity = function(doc,cdt,cdn){

	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){
		frappe.call({
            	    method:"samsungapp.samsungapp.doctype.buy_back_requisition.buy_back_requisition.get_capacity",
            	    args:{"capacity":doc.capacity,
            	           "active":doc.is_the_device_active},
            	    callback:function(r){
						if (r.message==0){
							doc.device_capacity=0.0
							refresh_field('device_capacity');
							cur_frm.cscript.update_totals(doc);
						}
						else if(r.message>0){
							value= r.message/100
							doc.device_capacity=value*doc.basic_price
							refresh_field('device_capacity');
							cur_frm.cscript.update_totals(doc);
						}
						
					}
			})
	}
	else{
		msgprint("Please specify device is activate or not");

	}
}



cur_frm.cscript.update_totals=function(doc,cdt,cdn){
	console.log("update totals")
	var total=0.0;
	total=doc.functional_defects+doc.device_active+doc.screen_condition+doc.body_condition+doc.accessories+doc.device_capacity
	var doc = locals[doc.doctype][doc.name];
	doc.estimated_price =doc.basic_price-total;
	doc.offered_price=doc.basic_price-total;
	console.log(doc.estimated_price)
	refresh_field('estimated_price');
	refresh_field('offered_price');

}

cur_frm.cscript.captured_device_image = function(doc, cdt, cdn){
	console.log("in the image");
	console.log(doc.captured_device_image)
	doc.image='<table style="width: 100%; table-layout: fixed;"><tr><td style="width:110px"><img src="'+doc.captured_device_image+'" width="100px"></td></tr></table>'
	// doc.image='<table style="width: 100%; table-layout: fixed;"><tr><td style="width:100px"><img src="'+doc.captured_device_image+'" width="100px"></td></tr></table>'
	refresh_field("image");
}

cur_frm.cscript.customer_image = function(doc, cdt, cdn){
	console.log("in the image");
	console.log(doc.cust_image)
	doc.cust_image='<table style="width: 100%; table-layout: fixed;"><tr><td style="width:110px"><img src="'+doc.customer_image+'" width="100px"></td></tr></table>'
	// doc.image='<table style="width:100%; table-layout: fixed;"><tr><td style="width:100px"><img src="'+doc.cust_image+'" width="100px"></td></tr></table>'
	refresh_field("cust_image");
}

cur_frm.cscript.estimated_price=cur_frm.cscript.offered_price = function(doc, cdt, cdn){
	if(doc.offered_price>doc.estimated_price)
	{
		msgprint(__("Offered Price Should be less than Estimated Price."));
		
	}
}
