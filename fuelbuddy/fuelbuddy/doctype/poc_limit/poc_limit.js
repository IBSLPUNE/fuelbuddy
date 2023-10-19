// Copyright (c) 2023, ibsl and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contact Limit', {
	limit:function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];

		if (child.limit <= 0){
		    frappe.throw(__('Please Set Credit Limit More Than 0'));
		}
		else {
		calculate_amount(frm);
	}}
});

var calculate_amount = function(frm) {
	let tl = frm.doc.poc_credit_limit || [];
	let total_credit_limit = 0;
	for(var i=0; i<tl.length; i++) {
		if (tl[i].limit) {
			total_credit_limit += tl[i].limit;
		}
	}
	var remaning_credit_limit = frm.doc.customer_credit_limit - total_credit_limit;
	frm.set_value("remaning_credit_limit", remaning_credit_limit);
};

frappe.ui.form.on('POC Limit',{
    customer:function(frm){
        frappe.db.get_doc('Customer', frm.doc.customer)
    .then(doc => {
        var tl = doc.credit_limits || [];
        let customer_credit_limit = 0;
        for(var i=0; i<tl.length; i++){
            if (tl[i].credit_limit){
                customer_credit_limit += tl[i].credit_limit;
            }
            else{
                frappe.throw(__('Please Set Customer Credit Limit'));
            }
            frm.set_value("customer_credit_limit",customer_credit_limit);
        }
    });
        
    }
});
frappe.ui.form.on('POC Wallet',{
    allocated_amount:function(frm,cdt,cdn){
        var d = locals[cdt][cdn];
        if (frm.is_new()){
        	d.current_amount = d.allocated_amount
        }
        frm.refresh_field("poc_wallet")
    }
});