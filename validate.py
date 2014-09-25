# -*- coding: utf-8 -*-
from osv import osv, fields
import time
from datetime import datetime
from docutils.nodes import table

def validate(self, cr, uid, context):
    '''
        Validate Functions
        self = Self Model - mdc.raworder1 | mdc.raworder2 | mdc.raworder3
    '''
    # Define dictionary for fieldnames
    cust_field = {"mdc.raworder1":"textbox13",
                  "mdc.raworder2":"custname2",
                  "mdc.raworder3":"custname3"}
    partner_search_field = {"mdc.raworder1":"name",
                         "mdc.raworder2":"name",
                         "mdc.raworder3":"ref"}
    prod_field = {"mdc.raworder1":"eanproductcode",
                  "mdc.raworder2":"custname2",
                  "mdc.raworder3":"custname3"}
    product_search_field = {"mdc.raworder1":"ean13",
                             "mdc.raworder2":"ean13",
                             "mdc.raworder3":"ean13"
                             }
    orderdate_field = {"mdc.raworder1":"podate",
                       "mdc.raworder2":"podate",
                       "mdc.raworder3":"podate"}
    
    deliverydate_field = {"mdc.raworder1":"deliverydate",
                       "mdc.raworder2":"deliverydate",
                       "mdc.raworder3":"deliverydate"}

    orderref_field = {"mdc.raworder1":"pono",
                       "mdc.raworder2":"pono",
                       "mdc.raworder3":"pono"}

    linenum_field = {"mdc.raworder1":"lineitemno_1",
                       "mdc.raworder2":"lineitemno_1",
                       "mdc.raworder3":"lineitemno_1"}
                
    prodqty_field = {"mdc.raworder1":"totorder",
                       "mdc.raworder2":"totorder",
                       "mdc.raworder3":"totorder"}
                
    prodprice_field = {"mdc.raworder1":"unitprice",
                       "mdc.raworder2":"unitprice",
                       "mdc.raworder3":"unitprice"}
    
    timestamp = time.strftime("%d %b %Y %H:%M:%S")
    log_msg = timestamp + "\nValidate data in raw order table(" + str(self._name) + ") started...\n"
    log_msg = log_msg + "\There are " + str(self.search(cr, uid, [])) + " records in " + str(self._name) + " table."

    # Read all data from res.partner and mdc_custmap
    partner = self.pool.get('res.partner')
    custmap = self.pool.get('mdc.custmap')
    products = self.pool.get('product.product')
    prodmap = self.pool.get('mdc.prodmap')
    all_cust = partner.read(cr, uid, partner.search(cr, uid, [('customer', '=', True)]), ['id', 'name', 'ref'])
    all_prod = products.read(cr, uid, products.search(cr, uid, [('active', '=', True)]), ['id', 'code', 'ean13', 'name.template'])
    all_custmap = custmap.read(cr, uid, custmap.search(cr, uid, [('srce_model', '=', self._name)]),
                               ['srce_cust_field', 'srce_cust_value', 'dest_cust_value'])
    all_prodmap = prodmap.read(cr, uid, prodmap.search(cr, uid, [('srce_model', '=', self._name)]),
                               ['srce_prod_field', 'srce_prod_value', 'dest_prod_value'])
            
    # Loop through each records on self
    for rec_id in self.search(cr, uid, []):
        # Initialize variables for this specific source records
        custmap_ok = False
        prodmap_ok = False
        mdcso_cust = ""
        mdcso_prod = ""
        validate_all_ok = False
        vldn_msg = timestamp + " Start Validating Customer..."
        
        # read customer & product value from raworder 
        cust_value = self.read(cr, uid, rec_id, [cust_field[self._name]])[cust_field[self._name]]
        prod_value = self.read(cr, uid, rec_id, [prod_field[self._name]])[prod_field[self._name]]
               
        # Check with all_cust if matched
        custmap_ok = False
        for cust_rec in all_cust:
            if custmap_ok:
                # If the customer has been found in earlier loop, then break
                break
            if cust_rec[partner_search_field[self._name]] == cust_value:
                vldn_msg = vldn_msg + "\nRaw Customer Value: " + cust_value + "  matched with " + \
                    cust_rec[partner_search_field[self._name]]
                mdcso_cust = cust_rec[partner_search_field[self._name]]
                custmap_ok = True
                break
            else:
                # Check against all_custmap
                for custmap_rec in all_custmap:
                    if (custmap_rec['srce_cust_field'] == partner_search_field[self._name]) and \
                        (custmap_rec['srce_cust_value'] == cust_value):
                        vldn_msg = vldn_msg + "\nRaw Customer Value: " + cust_value + "  matched with " + \
                            custmap_rec['dest_cust_value'] + " via Customer Mappping Table."
                        mdcso_cust = custmap_rec['dest_cust_value']
                        custmap_ok = True
                        break
                    else:
                        continue
                        
        if not custmap_ok: 
            mdcso_cust = ""
            vldn_msg = vldn_msg + "\n" + cust_value + " is INVALID CUSTOMER VALUE !!!"
        
        # Check with all_prod if matched
        prodmap_ok = False
        for prod_rec in all_prod:
            if prodmap_ok:
                # If the product has been found in earlier loop, then break
                break
            if prod_rec[product_search_field[self._name]] == prod_value:
                vldn_msg = vldn_msg + "\nRaw Product code: " + prod_value + " macthed with " + \
                    prod_rec[product_search_field[self._name]]
                mdcso_prod = prod_rec[product_search_field[self._name]]
                prodmap_ok = True
                break
            else:
                # Check against all_prodmap
                for prodmap_rec in all_prodmap:
                    if (prodmap_rec['srce_prod_field'] == product_search_field[self._name]) and \
                        (prodmap_rec['srce_prod_value'] == prod_value):
                        vldn_msg = vldn_msg + "\nRaw Product Value: " + prod_value + " matched with " + \
                            prodmap_rec['dest_prod_value'] + " via Product Mapping Table."
                        mdcso_prod = prodmap_rec['dest_prod_value']
                        prodmap_ok = True
                        break
                    else:
                        continue
        
        if not prodmap_ok:
            mdcso_prod = ""
            vldn_msg = vldn_msg + "\n" + prod_value + " is INVALID PRODUCT VALUE!!!"
        
        if custmap_ok and prodmap_ok:
            mdcvld_ok = True
            # Read other fields data
            cur_rec = self.read(cr, uid, rec_id, [
                                        orderdate_field[self._name],
                                        deliverydate_field[self._name],
                                        orderref_field[self._name],
                                        linenum_field[self._name],
                                        prodqty_field[self._name],
                                        prodprice_field[self._name]
                                        ])

            # assume orderdate and delivery date format as for Big C
            mdcso_orderdate = time.mktime(time.strptime(cur_rec[orderdate_field[self._name]][0:10],"%d/%m/%Y"))
            mdcso_deliverydate = time.mktime(time.strptime(cur_rec[deliverydate_field[self._name]][0:10],"%d/%m/%Y"))
            mdcso_orderdate = datetime.fromtimestamp(mdcso_orderdate)
            mdcso_deliverydate = datetime.fromtimestamp(mdcso_deliverydate)

            self.write(cr, uid, rec_id, {
                                     "mdcso_orderdate" : mdcso_orderdate,
                                     "mdcso_deliverydate" : mdcso_deliverydate,
                                     "mdcso_order_ref" : cur_rec[orderref_field[self._name]],
                                     "mdcso_prod_linenum" : cur_rec[linenum_field[self._name]],
                                     "mdcso_prod_qty" : int(float(cur_rec[prodqty_field[self._name]])),
                                     "mdcso_prod_price" : float(cur_rec[prodprice_field[self._name]])
                                     } , context)
            #print curr_rec.orderref_field[self._name]
            vldn_msg = vldn_msg + "\n\n Both customer and product valided successfully. Other fields populated"
        else:
            mdcvld_ok = False
            
        # Write the result of customer validation
        self.write(cr, uid, rec_id, {"mdcvld_date" : timestamp,
                                     "mdcvld_custmap_ok" : custmap_ok,
                                     "mdcvld_prodmap_ok" : prodmap_ok,
                                     "mdcvld_ok" : mdcvld_ok,
                                     "mdcso_customer" : mdcso_cust,
                                     "mdcso_cust_delivery" : mdcso_cust,
                                     "mdcso_cust_invoice" : mdcso_cust,
                                     "mdcso_prod_name" : mdcso_prod,
                                     "mdcvld_remark" : vldn_msg,                                  
                                     } , context)
        
    # Compose log message - summarizing validation results
    all_valid_count = self.search(cr, uid, [('mdcvld_ok','=',True)], offset=0, count=True)
    invalid_cust_count = self.search(cr, uid, [('mdcvld_custmap_ok','=',False)], offset=0, count=True)
    invalid_prod_count = self.search(cr, uid, [('mdcvld_prodmap_ok','=',False)], offset=0, count=True)
    log_msg = log_msg + "\nValidation Completed."
    log_msg = log_msg + "\nThere are " + str(all_valid_count) + " records that all valid"
    log_msg = log_msg + "\nThere are " + str(invalid_cust_count) + " records with invalid customer"
    log_msg = log_msg + "\nThere are " + str(invalid_prod_count) + " records with invalid product"
    
    # Construct list of invalid customers
    invalid_cust_list = set()
    for rec in self.search(cr, uid, [('mdcvld_custmap_ok','=',False)]):
        cust_value = self.read(cr, uid, rec, [cust_field[self._name]])[cust_field[self._name]]
        if cust_value not in invalid_cust_list:
            invalid_cust_list.add(cust_value)

    # Construct list of invalid products
    invalid_prod_list = set()
    for rec in self.search(cr, uid, [('mdcvld_prodmap_ok','=',False)]):
        prod_value = self.read(cr, uid, rec, [prod_field[self._name]])[prod_field[self._name]]
        if prod_value not in invalid_prod_list:        
            invalid_prod_list.add(prod_value)

    log_msg = log_msg + "\nThere are " + str(len(invalid_cust_list)) + " unique invlide customers:\n" + str(invalid_cust_list)
    log_msg = log_msg + "\nThere are " + str(len(invalid_prod_list)) + " unique invlide products:\n" + str(invalid_prod_list)
    
    
    # Write process log
    processlog = self.pool.get('mdc.processlog')
    processlog_value = {"srce_model" : str(self._name),
                        "process_name" : "Validate",
                        "process_date" : datetime.now(),
                        "log" : log_msg}
    processlog_rec = processlog.create(cr, uid, processlog_value,context)
 
