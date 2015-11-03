cur_frm.cscript.onload = function(doc, cdt, cdn){
	doc.company=frappe.defaults.get_user_default("company");
	doc.fiscal_year=frappe.defaults.get_user_default("fiscal_year");
	doc.date = doc.date||frappe.datetime.get_today();
	field=['date','company','fiscal_year']
	refresh_field('field');
}

cur_frm.cscript.channel=function(doc,dt,dn){
		cur_frm.set_df_property("sales_order", "reqd", doc.channel=="Matrix Device Repairs");
		cur_frm.set_df_property("purchase_receipt", "reqd", doc.channel=="Matrix Preowned");
}

cur_frm.cscript.sales_order=function(doc,dt,dn){
	if(doc.channel=="Matrix Device Repairs"){
			frappe.call({
            	    method:"samsungapp.samsungapp.doctype.device_repair.device_repair.get_customer",
            	    args:{
            	    	"sales_order":doc.sales_order
            		},
            	    callback:function(r){
            	    	if (r.message){
							doc.customer=r.message[0]
							var rp=r.message[1]
							refresh_field('customer');
							$.each(r.message[1], function(i, item) {
							var d = frappe.model.add_child(cur_frm.doc, "Sales Order Item", "repair_part");
							d.actual_qty = item.actual_qty;
							d.amount = item.amount;
							d.base_price_list_rate = item.base_price_list_rate;
							d.base_amount = item.base_amount;
							d.base_rate = item.base_rate;
							d.billed_amt = item.billed_amt;
							d.brand = item.brand;
							d.customer_item_code = item.customer_item_code;
							d.delivered_qty = item.delivered_qty;
							d.description = item.description;
							d.discount_percentage = item.discount_percentage;
							d.item_code = item.item_code;
							d.item_group = item.item_group;
							d.item_name = item.item_name;
							d.item_tax_rate = item.item_tax_rate;

							d.price_list_rate = item.price_list_rate;
							d.pricing_rule = item.pricing_rule;
							d.produced_qty = item.produced_qty;
							d.projected_qty = item.projected_qty;
							d.qty = item.qty;
							d.rate = item.rate;
							d.stock_uom = item.stock_uom;
							d.transaction_date = item.transaction_date;
							d.warehouse = item.warehouse;
							d.item_tax_rate = item.item_tax_rate;
							
						});
						refresh_field("repair_part");
														
						}
					}
        	})
		}
}

cur_frm.cscript.purchase_receipt=function(doc,dt,dn){
	if(doc.channel=="Matrix Preowned"){
		frappe.call({
    	    method:"samsungapp.samsungapp.doctype.device_repair.device_repair.get_item",
    	    args:{
    	    	"purchase_receipt":doc.purchase_receipt
    		},
    	    callback:function(r){
    	    	if (r.message)
    	    	{
					doc.dv=r.message;
					refresh_field("dv");								
				}
			}
    	})
	}
}