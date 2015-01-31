cur_frm.add_fetch("item_code", "item_name", "item_name");
cur_frm.add_fetch("customer", "customer_name", "customer_name");
cur_frm.add_fetch("customer", "email_id", "email_id");
cur_frm.add_fetch("customer", "phone_no", "phone_no");

cur_frm.add_fetch("item_code", "basic_price", "basic_price");

cur_frm.cscript.basic_price = function(doc,cdt,cdn){
	console.log("in basic price")
	doc.estimated_price=doc.basic_price
	refresh_field('estimated_price');
	refresh_field('device_active');
}

cur_frm.cscript.is_the_device_active = function(doc,cdt,cdn){
	if(doc.is_the_device_active=='Yes'){
		doc.estimated_price=doc.basic_price
		doc.device_active=0.0
		refresh_field('device_active');
		cur_frm.cscript.update_totals(doc);
	}
	else if(doc.is_the_device_active=='No'){
		price =(0.2*doc.basic_price)
		doc.device_active=0.0
		doc.basic_price=price
		doc.estimated_price=price
		refresh_field('device_active');
		refresh_field('basic_price');
		refresh_field('estimated_price');
		//cur_frm.cscript.update_totals(doc);
	}
}

cur_frm.cscript.does_it_have_any_functional_defects = function(doc,cdt,cdn){

	if (doc.is_the_device_active=='Yes'){

		if(doc.does_it_have_any_functional_defects=='Yes'){
				price =(0.2*doc.basic_price)
				doc.functional_defects=price
				refresh_field('functional_defects');
				cur_frm.cscript.update_totals(doc);	
		}
		else if(doc.does_it_have_any_functional_defects=='No'){
				doc.functional_defects=0.0
				refresh_field('functional_defects');
				cur_frm.cscript.update_totals(doc);
			
		}
	}
	else if (doc.is_the_device_active=='No'){
		if(doc.does_it_have_any_functional_defects=='Yes'){
				doc.functional_defects=0.0
				refresh_field('functional_defects');
				cur_frm.cscript.update_totals(doc);	
		}
		else if(doc.does_it_have_any_functional_defects=='No'){
				doc.functional_defects=0.0
				refresh_field('functional_defects');
				cur_frm.cscript.update_totals(doc);
			
		}
	}

	else{
		msgprint("Please specify device is activate or not");
	}

	}
	

cur_frm.cscript.condition_of_the_screen = function(doc,cdt,cdn){

	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){

		if(doc.condition_of_the_screen=='Broken Screen'){
			price=(0.3*doc.basic_price)
			doc.screen_condition=price
			refresh_field('screen_condition')
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.condition_of_the_screen=='Poor'){
			price=(0.2*doc.basic_price)
			doc.screen_condition=price
			refresh_field('screen_condition')
			cur_frm.cscript.update_totals(doc);
		}

		else if (doc.condition_of_the_screen=='Just OK'){
			price=(0.15*doc.basic_price)
			doc.screen_condition=price
			refresh_field('screen_condition')
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.condition_of_the_screen=='Excellent'){
			doc.screen_condition=0.0
			refresh_field('screen_condition');
			cur_frm.cscript.update_totals(doc);
		}

	}

	else{
		msgprint("Please specify device is activate or not");
	}
}

cur_frm.cscript.condition_of_device_body = function(doc,cdt,cdn){

	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){

		if(doc.condition_of_device_body=='Poor'){
			price=(0.2*doc.basic_price)
			doc.body_condition=price
			refresh_field('body_condition');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.condition_of_device_body=='Just OK'){
			price=(0.15*doc.basic_price)
			doc.body_condition=price
			refresh_field('body_condition');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.condition_of_device_body=='Excellent'){
			doc.body_condition=0.0
			refresh_field('body_condition')
			cur_frm.cscript.update_totals(doc);
		}
	}

	else{
		msgprint("Please specify device is activate or not");

	}
}

cur_frm.cscript.accessories_included = function(doc,cdt,cdn){
	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){
		if (doc.accessories_included=='Yes'){
			doc.accessories=0.0
			refresh_field('accessories')
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.accessories_included=='No'){
			price=(0.05*doc.basic_price)
			doc.accessories=price
			refresh_field('accessories')
			cur_frm.cscript.update_totals(doc);
		}
	}
	else{
		msgprint("Please specify device is activate or not");

	}
}

cur_frm.cscript.capacity = function(doc,cdt,cdn){

	if (doc.is_the_device_active=='Yes' || doc.is_the_device_active=='No'){

		if (doc.capacity=='8GB'){
			price=(0.05*doc.basic_price)
			doc.device_capacity=price
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.capacity=='16GB'){
			price=(0.03*doc.basic_price)
			doc.device_capacity=price
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.capacity=='32GB'){
			price=(0.02*doc.basic_price)
			doc.device_capacity=price
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.capacity=='64GB'){
			price=(0.01*doc.basic_price)
			doc.device_capacity=price
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.capacity=='128GB'){
			doc.device_capacity=0.0
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
		else if (doc.capacity=='N/A'){
			doc.device_capacity=0.0
			refresh_field('device_capacity');
			cur_frm.cscript.update_totals(doc);
		}
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
	console.log(doc.estimated_price)
	refresh_field('estimated_price');

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
