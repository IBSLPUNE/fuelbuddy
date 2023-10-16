import frappe

@frappe.whitelist()
def chem():
    if doc.customer_type == 'Company':
        for i in doc.get('point_of_contact'):
            if frappe.db.exists("Contact", i.contact):
                con = frappe.get_doc('Contact',i.contact)
                con.append("links",{
                    "link_doctype":"Lead",
                    "link_name":doc.name
                    })
                con.save()
    if doc.customer_type == 'Individual':
        if frappe.db.exists("Contact", doc.individual):
            con = frappe.get_doc('Contact',doc.individual)
            con.append("links",{
                "link_doctype":"Lead",
                "link_name":doc.name
                })
                con.save()

# contact = frappe.db.get_list('Dynamic Link',filters={
#     'link_name':doc.name,
#     'link_doctype':'Lead'
#     },fields='parent',pluck='parent')
# if contact != []:
#     for i in contact:
#         frappe.delete_doc('Contact', i)










@frappe.whitelist()
def test():
    contacts = frappe.db.get_list('Contact',filters={
        "contact_state":"Automatic"
        },
        pluck='name')
    for i in contacts:
        frappe.delete_doc('Contact', i)