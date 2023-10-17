import frappe


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




def sdf():
    cust = doc.customer
    cont = doc.contact_person
    # nam = doc.item_name
    # frappe.throw(nam)
    for i in doc.items:
        item = i.item_code
        # item_name = item.item_name
        quantity = i.qty

        # v = (f"{item}")
        # h = (f"{quantity}")
        # b = (f"{item_name}")
    # frappe.throw(str(quantity))


    if doc.source_of_creation == "ERP":    

        docs = frappe.new_doc('Delivery Fees Cal')
        docs.customer = cust
        docs.contact = cont
        docs.item = item
        # docs.item_name = item_name
        docs.qty = int(quantity)
#     # doc.password = password
        docs.insert()
        if docs.df == None:
            doc.append("items", {
                "item_code": "STO-ITEM-2023-00014",
                "qty": 1,
                # "item_name" : "Standard Delivery Fees",
                "rate": int(quantity),
                "delivery_date": doc.delivery_date,
                "amount": int(quantity)
            })
            doc.run_method("set_missing_values")
            doc.save()
        else:
            doc.append("items", {
                "item_code": "STO-ITEM-2023-00014",
                "qty": 1,
                # "item_name" : "Standard Delivery Fees",
                "rate": docs.df,
                "delivery_date": doc.delivery_date,
                "amount": docs.df * 1
                })
            doc.run_method("set_missing_values")
            doc.save()




def supplier_onboarding():
    so = frappe.get_doc("Supplier Onboarding",doc.ro_onboarding)
    if so.adhoc == 1:
        abbr = "A"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_doc("Warehouse")
            warehouse.field_name = doc.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.business_partner == 1:
        abbr = "BP"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_doc("Warehouse")
            warehouse.field_name = doc.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.delivery_partner == 1:
        abbr = "DP"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_doc("Warehouse")
            warehouse.field_name = doc.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.direct == 1:
        abbr = "D"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_doc("Warehouse")
            warehouse.field_name = doc.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()


def margin():
    margin = frappe.db.get_value("Warehouse",doc.set_warehouse,'margin')
    doc.appenmd('taxes',{
        "account_head":"Operational Income - F",
        "rate":float(margin)})
    doc.save()


def Delivery Fees Calculations():
    #Standard Delivery Fees
    if frappe.db.exists("Delivery Fees", {"contact": doc.contact,"address":doc.address}):
        df = frappe.get_doc('Delivery Fees',frappe.db.exists("Delivery Fees", {"contact": doc.contact,"address":doc.address}))
        if df.dt == 'Standard Delivery Fees':
            if doc.qty>199:
                doc.df = float(doc.qty * float(df.standard_fees))
            else:
                doc.df = 199
        elif df.dt == 'Fixed Delivery Fees':
            doc.df = float(df.fixed_fee)
        elif df.dt == 'Variable Delivery Fees':
            if float(doc.qty) - float(df.upto_qty) <= 0:
                if float(df.upto_rate) ==0:
                    doc.df = float(df.upto_fixed_amount)
                elif float(df.upto_fixed_amount) ==0:
                    doc.df = float(df.upto_rate) * float(doc.qty)
                    if doc.df<199:
                        doc.df=199
            else:
                left = float(doc.qty) - float(df.upto_qty)
                if float(df.upto_fixed_amount)==0:
                    if float(df.above_fixed_amount) ==0:
                        doc.df = (float(df.upto_qty) * float(df.upto_rate)) + (float(df.above_rate) * left)
                    else:
                        doc.df = (float(df.upto_qty) * float(df.upto_rate)) + float(df.above_fixed_amount)
                else:
                    if float(df.above_fixed_amount) ==0:
                        doc.df = float(df.upto_fixed_amount) + (float(df.above_rate) * left)
                    else:
                        doc.df = float(df.upto_fixed_amount) + float(df.above_fixed_amount)
                if doc.df <199:
                    doc.df=199


def POC():
    credit_limit = frappe.db.get_value("Contact Limit",{'parent':doc.customer,'contact':doc.contact_person},"limit")
    if credit_limit != None:
        doc.poc_credit_limit = credit_limit
        credits = frappe.db.get_list("Sales Order",
            filters={
                'status': ['not in', 'Completed, Draft, To Bill ,Cancelled'],
                'contact_person':doc.contact_person
            },
            fields='grand_total',
            pluck="grand_total"
            )
        total_credit = 0
        for c in credits:
            total_credit = total_credit+c
        poc_remaining_credit_limit = credit_limit - total_credit
        doc.poc_remaining_credit_limit = credit_limit - total_credit
        if doc.grand_total >poc_remaining_credit_limit and doc.credit_breach == 0:
            frappe.throw("Credit Limit Is Breached")
    

def journal_entry():
    frappe.errprint(doc)



def oap():
    if doc.workflow_state == "Pending by Operations Team":
        frappe.db.set_value('Opportunity', doc.opportunity, 'activity_', '6.Ops Approval Pending')
        frappe.db.set_value('Opportunity', doc.opportunity, 'sales_stage', 'Ops Approval Pending')
        op = frappe.get_doc("Opportunity",doc.opportunity)
        op.reload()
        


def oauf():
    if doc.workflow_state == "Pending by CRM Finance":
        appe.db.set_value('Opportunity', doc.opportunity, 'activity_', '4.Finance Approval Pending')
        frappe.db.set_value('Opportunity', doc.opportunity, 'sales_stage', 'Finance Approval Pending')
        op = frappe.get_doc("Opportunity",doc.opportunity)
        op.reload()
    
def on_boarding():
    if frappe.db.exists("Opportunity",doc.opportunity_name):
        opportunity = frappe.get_doc("Opportunity",doc.opportunity_name)
        opportunity.activity_ = "9.On-boarded"
        opportunity.sales_stage = "On-boarded"
        opportunity.save()

def party_balance():
    select_field = "sum(debit_in_account_currency) - sum(credit_in_account_currency)"
    gl = frappe.db.get_list("GL Entry",filters={'is_cancelled':0,'party_type' : 'Customer','party':doc.customer},fields = "credit_in_account_currency",pluck = "credit_in_account_currency")
    party_balance = 0.0
    for i in gl:
        party_balance = party_balance + i
    so = frappe.db.get_list("Sales Order",filters={"customer":doc.customer,"docstatus":1},fields=["grand_total"],pluck="grand_total")
    total_so = 0.0
    for i in so:
        total_so = total_so + i
    total= party_balance - total_so
    doc.party_balance = total

def lead_cl():
    doc.referred_by = frappe.db.get_value("Lead",doc.lead_name,"referred_by")


def ggl_ec():
    voucher = ["Sales Invoice","Payment Entry","Purchase Entry"]
    if doc.voucher_type in voucher:
        doc.contact = frappe.db.get_value(doc.voucher_type,doc.voucher_no,'contact_person')

def activity():
    activity = frappe.get_doc("Activity at Opportunity",doc.activity_)
    if doc.serial_number == "" or doc.serial_number == None:
        doc.serial_number = activity.serial_number
    if activity.serial_number <doc.serial_number:
        frappe.throw("Cannot Go Back To Previous Activity")
    if activity.serial_number >doc.serial_number:
        doc.serial_number = activity.serial_number

def item_opportunity():
    if len(doc.get('items')) == 0:
        doc.append('items',{
            "item_code":doc.fuel_type,
            "uom":doc.uom,
            "qty":doc.qty,  
            "rate":doc.rate,
            "base_rate":doc.rate,
            "base_amount":doc.base_opportunity_amount,
            "amount":doc.opportunity_amount
        })
 


def address_validation():
    state= frappe.db.get_value("City",doc.city_,"state")
    if state != doc.state_:
        frappe.throw("State is Invalid")


def full_name():
    if doc.first_name != None and doc.last_name == None:
        doc.full_name = doc.first_name
    else:
        doc.full_name = doc.first_name +" "+ doc.last_name

    leads = frappe.db.get_list('Lead',filters={
        "individual":doc.name,
        
    },pluck='name')
    for i in leads:
        lead = frappe.get_doc('Lead',i)
        lead.db_set('first_name',doc.first_name)
        lead.db_set('last_name',doc.last_name)
        lead.db_set('lead_name',doc.full_name)
        lead.db_set('title',doc.full_name)
        lead.run_method('validate')
        lead.reload()

