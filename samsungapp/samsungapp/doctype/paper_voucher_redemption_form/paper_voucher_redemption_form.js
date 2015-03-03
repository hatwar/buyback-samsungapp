
cur_frm.cscript.onload = function(doc, cdt, cdn) {
	cur_frm.cscript.get_warehouse(doc, cdt, cdn)
}


cur_frm.cscript.get_warehouse = function(doc, cdt, cdn) {
	return cur_frm.call({
			doc: cur_frm.doc,
			method: "get_warehouse",
			callback: function(r) {
				if(r.message) {
                cur_frm.set_value("warehouse", r.message['warehouse']);
                refresh_field('warehouse')
                					

				} 
			}
		})
}		



