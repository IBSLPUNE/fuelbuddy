import frappe


def chem(self,method):
    if self.customer_type == 'Company':
        for i in self.get('point_of_contact'):
            if frappe.db.exists("Contact", i.contact):
                con = frappe.get_self('Contact',i.contact)
                con.append("links",{
                    "link_selftype":"Lead",
                    "link_name":self.name
                    })
                con.save()
    if self.customer_type == 'Individual':
        if frappe.db.exists("Contact", self.individual):
            con = frappe.get_self('Contact',self.individual)
            con.append("links",{
                "link_selftype":"Lead",
                "link_name":self.name
                })
            con.save()

# contact = frappe.db.get_list('Dynamic Link',filters={
#     'link_name':self.name,
#     'link_selftype':'Lead'
#     },fields='parent',pluck='parent')
# if contact != []:
#     for i in contact:
#         frappe.delete_self('Contact', i)

def sales_partner_creation(self,method):
    if self.transactional_diesel == 1 or self.transactional_petrol == 1:
        sales_partner = frappe.new_doc("Sales Partner")
        sales_partner.supplier = self.name
        sales_partner.transaction_type = self.transaction_type
        for i in sales_partner.get("sales_partner_commission_table"):
            if self.transactional_diesel == 1:
                i.item = "Diesel"
                i.commission = self.transactional__margin_diesel
            if self.transactional_petrol == 1:
                i.item = "Petrol"
                i.commission = self.transactional__margin_petrol

#Wallet Creation

def payment_entry(self,method):
    if self.party_type == "Customer" and self.payment_type == "Receive":
        payment_type = frappe.db.get_value("Customer",self.party,"payment_type")
        if payment_type == "Prepaid" and self.docstatus == 1:
            poclimit = frappe.db.get_value("POC Limit",{'customer':self.party},"name")
            doc = frappe.get_doc("POC Limit",poclimit)
            # Calculate wallet_amount using the absolute value of party_balance
            doc.wallet_amount = abs(self.party_balance) + self.paid_amount
            doc.save()

def sales_invoice(self,method):
    payment_type = frappe.db.get_value("Customer",self.customer,"payment_type")
    if payment_type == "Prepaid":
        poclimit = frappe.db.get_value("POC Limit",self.customer,"name")
        doc =frappe.get_doc("POC Limit",poclimit)
        for i in doc.get("poc_wallet"):
            if self.contact_person == i.poc:   
                i.current_amount = i.allocated_amount
        doc.save()
def sales_order(self,method):
    payment_type = frappe.db.get_value("Customer",self.customer,"payment_type")
    if payment_type == "Prepaid":
        poclimit = frappe.db.get_value("POC Limit",self.customer,"name")
        doc =frappe.get_doc("POC Limit",poclimit)
        doc.wallet_amount = doc.wallet_amount - self.base_grand_total
        for i in doc.get("poc_wallet"):
            if self.contact_person == i.poc:
                i.current_amount = i.current_amount - self.base_grand_total
        doc.save()

def sales_order_can(self,method):
    payment_type = frappe.db.get_value("Customer",self.customer,"payment_type")
    if payment_type == "Prepaid":
        poclimit = frappe.db.get_value("POC Limit",self.customer,"name")
        doc =frappe.get_doc("POC Limit",poclimit)
        doc.wallet_amount = doc.wallet_amount + self.base_grand_total
        for i in doc.get("poc_wallet"):
            if self.contact_person == i.poc:
                i.current_amount = i.current_amount + self.base_grand_total
        doc.save()

def salesorder_low_balance(self,method):
    payment_type = frappe.db.get_value("Customer",self.customer,"payment_type")
    if payment_type == "Prepaid":
        poclimit = frappe.db.get_value("POC Limit",self.customer,"name")
        doc =frappe.get_doc("POC Limit",poclimit)
        doc.wallet_amount = doc.wallet_amount - self.base_grand_total
        if doc.wallet_amount <0:
            frappe.throw("Please Do Payment First")
        for i in doc.get("poc_wallet"):
            if self.contact_person == i.poc and self.base_grand_total > i.current_amount and i.allocated_amount !=0:
                frappe.throw("Allocated Limit Crossed")

#Wallet Creation End

def sdf(self,method):
    cust = self.customer
    cont = self.contact_person
    # nam = self.item_name
    # frappe.throw(nam)
    for i in self.items:
        item = i.item_code
        # item_name = item.item_name
        quantity = i.qty

        # v = (f"{item}")
        # h = (f"{quantity}")
        # b = (f"{item_name}")
    # frappe.throw(str(quantity))


    if self.source_of_creation == "ERP":    

        selfs = frappe.new_self('Delivery Fees Cal')
        selfs.customer = cust
        selfs.contact = cont
        selfs.item = item
        # selfs.item_name = item_name
        selfs.qty = int(quantity)
#     # self.password = password
        selfs.insert()
        if selfs.df == None:
            self.append("items", {
                "item_code": "STO-ITEM-2023-00014",
                "qty": 1,
                # "item_name" : "Standard Delivery Fees",
                "rate": int(quantity),
                "delivery_date": self.delivery_date,
                "amount": int(quantity)
            })
            self.run_method("set_missing_values")
            self.save()
        else:
            self.append("items", {
                "item_code": "STO-ITEM-2023-00014",
                "qty": 1,
                # "item_name" : "Standard Delivery Fees",
                "rate": selfs.df,
                "delivery_date": self.delivery_date,
                "amount": selfs.df * 1
                })
            self.run_method("set_missing_values")
            self.save()




def supplier_onboarding(self,method):
    so = frappe.get_self("Supplier Onboarding",self.ro_onboarding)
    if so.adhoc == 1:
        abbr = "A"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_self("Warehouse")
            warehouse.field_name = self.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.business_partner == 1:
        abbr = "BP"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_self("Warehouse")
            warehouse.field_name = self.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.delivery_partner == 1:
        abbr = "DP"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_self("Warehouse")
            warehouse.field_name = self.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()
    if so.direct == 1:
        abbr = "D"
        for i in so.supplier_vehicle_table:
            warehouse = frappe.new_self("Warehouse")
            warehouse.field_name = self.supplier_fieldname
            warehouse.parent_warehouse = i.warehouse
            warehouse.warehouse_name = str(i.vehicle_number) + " - " + abbr 
            warehouse.vehicle_number = i.vehicle_number
            warehouse.insert()


def margin(self,method):
    margin = frappe.db.get_value("Warehouse",self.set_warehouse,'margin')
    self.appenmd('taxes',{
        "account_head":"Operational Income - F",
        "rate":float(margin)})
    self.save()


def delivery_fees_calculations(self,method):
    #Standard Delivery Fees
    if frappe.db.exists("Delivery Fees", {"contact": self.contact,"address":self.address}):
        df = frappe.get_self('Delivery Fees',frappe.db.exists("Delivery Fees", {"contact": self.contact,"address":self.address}))
        if df.dt == 'Standard Delivery Fees':
            if self.qty>199:
                self.df = float(self.qty * float(df.standard_fees))
            else:
                self.df = 199
        elif df.dt == 'Fixed Delivery Fees':
            self.df = float(df.fixed_fee)
        elif df.dt == 'Variable Delivery Fees':
            if float(self.qty) - float(df.upto_qty) <= 0:
                if float(df.upto_rate) ==0:
                    self.df = float(df.upto_fixed_amount)
                elif float(df.upto_fixed_amount) ==0:
                    self.df = float(df.upto_rate) * float(self.qty)
                    if self.df<199:
                        self.df=199
            else:
                left = float(self.qty) - float(df.upto_qty)
                if float(df.upto_fixed_amount)==0:
                    if float(df.above_fixed_amount) ==0:
                        self.df = (float(df.upto_qty) * float(df.upto_rate)) + (float(df.above_rate) * left)
                    else:
                        self.df = (float(df.upto_qty) * float(df.upto_rate)) + float(df.above_fixed_amount)
                else:
                    if float(df.above_fixed_amount) ==0:
                        self.df = float(df.upto_fixed_amount) + (float(df.above_rate) * left)
                    else:
                        self.df = float(df.upto_fixed_amount) + float(df.above_fixed_amount)
                if self.df <199:
                    self.df=199


def poc(self,method):
    credit_limit = frappe.db.get_value("Contact Limit",{'parent':self.customer,'contact':self.contact_person},"limit")
    if credit_limit != None:
        self.poc_credit_limit = credit_limit
        credits = frappe.db.get_list("Sales Order",
            filters={
                'status': ['not in', 'Completed, Draft, To Bill ,Cancelled'],
                'contact_person':self.contact_person
            },
            fields='grand_total',
            pluck="grand_total"
            )
        total_credit = 0
        for c in credits:
            total_credit = total_credit+c
        poc_remaining_credit_limit = credit_limit - total_credit
        self.poc_remaining_credit_limit = credit_limit - total_credit
        if self.grand_total >poc_remaining_credit_limit and self.credit_breach == 0:
            frappe.throw("Credit Limit Is Breached")
    

def journal_entry(self,method):
    frappe.errprint(self)



def oap(self,method):
    if self.workflow_state == "Pending by Operations Team":
        frappe.db.set_value('Opportunity', self.opportunity, 'activity_', '6.Ops Approval Pending')
        frappe.db.set_value('Opportunity', self.opportunity, 'sales_stage', 'Ops Approval Pending')
        op = frappe.get_self("Opportunity",self.opportunity)
        op.reload()
        


def oauf(self,method):
    if self.workflow_state == "Pending by CRM Finance":
        appe.db.set_value('Opportunity', self.opportunity, 'activity_', '4.Finance Approval Pending')
        frappe.db.set_value('Opportunity', self.opportunity, 'sales_stage', 'Finance Approval Pending')
        op = frappe.get_self("Opportunity",self.opportunity)
        op.reload()
    
def on_boarding(self,method):
    if frappe.db.exists("Opportunity",self.opportunity_name):
        opportunity = frappe.get_self("Opportunity",self.opportunity_name)
        opportunity.activity_ = "9.On-boarded"
        opportunity.sales_stage = "On-boarded"
        opportunity.save()

def party_balance(self,method):
    select_field = "sum(debit_in_account_currency) - sum(credit_in_account_currency)"
    gl = frappe.db.get_list("GL Entry",filters={'is_cancelled':0,'party_type' : 'Customer','party':self.customer},fields = "credit_in_account_currency",pluck = "credit_in_account_currency")
    party_balance = 0.0
    for i in gl:
        party_balance = party_balance + i
    so = frappe.db.get_list("Sales Order",filters={"customer":self.customer,"selfstatus":1},fields=["grand_total"],pluck="grand_total")
    total_so = 0.0
    for i in so:
        total_so = total_so + i
    total= party_balance - total_so
    self.party_balance = total

def lead_cl(self,method):
    self.referred_by = frappe.db.get_value("Lead",self.lead_name,"referred_by")


def ggl_ec(self,method):
    voucher = ["Sales Invoice","Payment Entry","Purchase Entry"]
    if self.voucher_type in voucher:
        self.contact = frappe.db.get_value(self.voucher_type,self.voucher_no,'contact_person')

def activity(self,method):
    activity = frappe.get_self("Activity at Opportunity",self.activity_)
    if self.serial_number == "" or self.serial_number == None:
        self.serial_number = activity.serial_number
    if activity.serial_number <self.serial_number:
        frappe.throw("Cannot Go Back To Previous Activity")
    if activity.serial_number >self.serial_number:
        self.serial_number = activity.serial_number

def item_opportunity(self,method):
    if len(self.get('items')) == 0:
        self.append('items',{
            "item_code":self.fuel_type,
            "uom":self.uom,
            "qty":self.qty,  
            "rate":self.rate,
            "base_rate":self.rate,
            "base_amount":self.base_opportunity_amount,
            "amount":self.opportunity_amount
        })
 


def address_validation(self,method):
    state= frappe.db.get_value("City",self.city_,"state")
    if state != self.state_:
        frappe.throw("State is Invalid")


def full_name(self,method):
    if self.first_name != None and self.last_name == None:
        self.full_name = self.first_name
    else:
        self.full_name = self.first_name +" "+ self.last_name

    leads = frappe.db.get_list('Lead',filters={
        "individual":self.name,
        
    },pluck='name')
    for i in leads:
        lead = frappe.get_self('Lead',i)
        lead.db_set('first_name',self.first_name)
        lead.db_set('last_name',self.last_name)
        lead.db_set('lead_name',self.full_name)
        lead.db_set('title',self.full_name)
        lead.run_method('validate')
        lead.reload()

