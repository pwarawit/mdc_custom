# -*- coding: utf-8 -*-
from osv import osv, fields
import time
from datetime import datetime
from openerp.tools.translate import _

def validate(self, cr, uid, context):
    '''
        Validate Functions
        self = Self Model - mdc.order.bigc | mdc.raworder2 | mdc.raworder3
    '''
    
    def mapcust(self, cr, uid, all_cust, all_custmap, ordermap_rec, cust_value):
        # Function to find mapping customers - by first searching all_custmap, then all_cust based on cust_value
        ''' Return list of custmap_ok and mapped cust value (mdcso_cust)'''
        custmap_ok = False
        mdcso_cust = ''
        # Search custmap first, if the mapping exist, replace cust_value with mapped value
        for custmap_rec in all_custmap:
            if custmap_rec['srce_cust_value'] == cust_value:
                # Mapping found, replace cust_value with the mapped value
                cust_value = custmap_rec['dest_cust_value']
                break
        
        # Now search all_cust for cust_value
        for cust_rec in all_cust:
            if cust_rec[ordermap_rec.map_cust] == cust_value:
                # Found the customer
                custmap_ok = True
                mdcso_cust = cust_rec[ordermap_rec.key_cust]
                break

        return [custmap_ok, mdcso_cust]
    
    # Read the order_map setting into ordermap_rec 
    ordermap = self.pool.get('mdc.ordermap') 
    ordermap_rec = ordermap.browse(cr, uid, ordermap.search(cr, uid, [('name','=',self._name[10:])]))
# 
#     orderdate_field = {"mdc.order.bigc":"podate",
#                        "mdc.raworder2":"podate",
#                        "mdc.raworder3":"podate"}
#     
#     deliverydate_field = {"mdc.order.bigc":"deliverydate",
#                        "mdc.raworder2":"deliverydate",
#                        "mdc.raworder3":"deliverydate"}

    linenum_field = {"mdc.order.bigc":"lineitemno_1",
                       "mdc.raworder2":"lineitemno_1",
                       "mdc.raworder3":"lineitemno_1"}
                
    prodqty_field = {"mdc.order.bigc":"totorder",
                       "mdc.raworder2":"totorder",
                       "mdc.raworder3":"totorder"}
                
    prodprice_field = {"mdc.order.bigc":"unitprice",
                       "mdc.raworder2":"unitprice",
                       "mdc.raworder3":"unitprice"}
    
    timestamp = time.strftime("%d %b %Y %H:%M:%S")
    log_msg = timestamp + "\nValidate data in raw order table(" + str(self._name) + ") started...\n"
    log_msg = log_msg + "There are " + str(len(self.search(cr, uid, []))) + " records in " + str(self._name) + " table."

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
        vldn_msg = timestamp # + " Start Validating Customer..."
        
        # read customer & product value from raworder 
        cust_value = self.read(cr, uid, rec_id, [ordermap_rec[0].order_cust])[ordermap_rec[0].order_cust]
        cust_ship_value = self.read(cr, uid, rec_id, [ordermap_rec[0].order_cust_ship])[ordermap_rec[0].order_cust_ship]
        cust_inv_value = self.read(cr, uid, rec_id, [ordermap_rec[0].order_cust_inv])[ordermap_rec[0].order_cust_inv]
        prod_value = self.read(cr, uid, rec_id, [ordermap_rec[0].order_prod])[ordermap_rec[0].order_prod]
        
        custmap_result = mapcust(self, cr, uid, all_cust, all_custmap, ordermap_rec[0], cust_value)
        custmap_ship_result = mapcust(self, cr, uid, all_cust, all_custmap, ordermap_rec[0], cust_ship_value)
        custmap_inv_result = mapcust(self, cr, uid, all_cust, all_custmap, ordermap_rec[0], cust_inv_value)
        
        vldn_msg = vldn_msg + "\n  Customer:" + cust_value 
        if custmap_result[0]:
            vldn_msg = vldn_msg + "   -- Matched with " + custmap_result[1]
        else: 
            vldn_msg = vldn_msg + "   -- Invalid !!! "

        vldn_msg = vldn_msg + "\n  Shipping Customer:" + cust_ship_value 
        if custmap_ship_result[0]:
            vldn_msg = vldn_msg + "   -- Matched with " + custmap_ship_result[1]
        else: 
            vldn_msg = vldn_msg + "   -- Invalid !!! "

        vldn_msg = vldn_msg + "\n  Invoicing Customer:" + cust_inv_value 
        if custmap_inv_result[0]:
            vldn_msg = vldn_msg + "   -- Matched with " + custmap_inv_result[1]
        else: 
            vldn_msg = vldn_msg + "   -- Invalid !!! "
            
        custmap_ok = custmap_result[0] and custmap_ship_result[0] and custmap_inv_result[0]
        
        # Check with all_prod if matched
        prodmap_ok = False
        for prod_rec in all_prod:
            if prodmap_ok:
                # If the product has been found in earlier loop, then break
                break
            if prod_rec[ordermap_rec[0].map_prod] == prod_value:
                vldn_msg = vldn_msg + "\nRaw Product code: " + prod_value + " macthed with " + \
                    prod_rec[ordermap_rec[0].map_prod]
                mdcso_prod = prod_rec[ordermap_rec[0].map_prod]
                prodmap_ok = True
                break
            else:
                # Check against all_prodmap
                for prodmap_rec in all_prodmap:
                    if (prodmap_rec['srce_prod_field'] == ordermap_rec[0].map_prod) and \
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
                                        ordermap_rec[0].order_date,
                                        ordermap_rec[0].order_delivery_date,
                                        ordermap_rec[0].order_ref,
                                        linenum_field[self._name],
                                        prodqty_field[self._name],
                                        prodprice_field[self._name]
                                        ])

            # assume orderdate and delivery date format as for Big C
            mdcso_orderdate = time.mktime(time.strptime(cur_rec[ordermap_rec[0].order_date][0:10],"%d/%m/%Y"))
            mdcso_deliverydate = time.mktime(time.strptime(cur_rec[ordermap_rec[0].order_delivery_date][0:10],"%d/%m/%Y"))
            mdcso_orderdate = datetime.fromtimestamp(mdcso_orderdate)
            mdcso_deliverydate = datetime.fromtimestamp(mdcso_deliverydate)

            self.write(cr, uid, rec_id, {
                                     "mdcso_orderdate" : mdcso_orderdate,
                                     "mdcso_deliverydate" : mdcso_deliverydate,
                                     "mdcso_order_ref" : cur_rec[ordermap_rec[0].order_ref],
                                     "mdcso_prod_linenum" : cur_rec[linenum_field[self._name]],
                                     "mdcso_prod_qty" : int(float(cur_rec[prodqty_field[self._name]].replace(',', ''))),
                                     "mdcso_prod_price" : float(cur_rec[prodprice_field[self._name]].replace(',', ''))
                                     } , context)
            #print curr_rec.ordermap_rec[0].order_ref
            vldn_msg = vldn_msg + "\n\n Both customer and product valided successfully. Other fields populated"
        else:
            mdcvld_ok = False
            
        # Write the result of customer validation
        self.write(cr, uid, rec_id, {"mdcvld_date" : timestamp,
                                     "mdcvld_custmap_ok" : custmap_ok,
                                     "mdcvld_prodmap_ok" : prodmap_ok,
                                     "mdcvld_ok" : mdcvld_ok,
                                     "mdcso_customer" : custmap_result[1],
                                     "mdcso_cust_delivery" : custmap_ship_result[1],
                                     "mdcso_cust_invoice" : custmap_inv_result[1],
                                     "mdcso_prod_name" : mdcso_prod,
                                     "mdcvld_remark" : vldn_msg,                                  
                                     } , context)
        
    # Compose log message - summarizing validation results
    all_valid_count = self.search(cr, uid, [('mdcvld_ok','=',True)], offset=0, count=True)
    invalid_cust_count = self.search(cr, uid, [('mdcvld_custmap_ok','=',False)], offset=0, count=True)
    invalid_prod_count = self.search(cr, uid, [('mdcvld_prodmap_ok','=',False)], offset=0, count=True)
    log_msg = log_msg + "\n\nValidation Completed."
    log_msg = log_msg + "\nThere are " + str(all_valid_count) + " records that all valid"
    log_msg = log_msg + "\nThere are " + str(invalid_cust_count) + " records with invalid customer"
    log_msg = log_msg + "\nThere are " + str(invalid_prod_count) + " records with invalid product"
    
    # Analyze the POs in the raw order
    po_list = set()
    for rec in self.search(cr, uid, []):
        po_value = self.read(cr, uid, rec, [ordermap_rec[0].order_ref])[ordermap_rec[0].order_ref]
        if po_value not in po_list:
            po_list.add(po_value)
    
    log_msg = log_msg + "\n\nThere are " + str(len(po_list)) + " orders: "
    for x in sorted(po_list):
        log_msg = log_msg + "\n Order Number : " + x
        poline_count = self.search(cr, uid, [(ordermap_rec[0].order_ref, '=', str(x))], offset=0, count=True)
        log_msg = log_msg + "  contains " + str(poline_count) + " lines."
        
        # Check if within PO - are all lines valid?
        invalid_line_count = self.search(cr, uid, [('mdcvld_ok','=',False),
                                                   (ordermap_rec[0].order_ref, '=', str(x))], offset=0, count=True)
        if invalid_line_count == 0:
            log_msg = log_msg + "  All order lines are valid."
        else:
            # There is at least 1 invalid line
            invalid_cust_list = set()
            invalid_prod_list = set()
            for invalid_rec in self.search(cr, uid, [('mdcvld_ok','=',False)
                                                     , (ordermap_rec[0].order_ref, '=', str(x))]):
                if not self.browse(cr, uid, invalid_rec).mdcvld_custmap_ok:
                    invalid_cust_list.add(self.read(cr, uid, invalid_rec, 
                                                    [ordermap_rec[0].order_cust])[ordermap_rec[0].order_cust])
                if not self.browse(cr, uid, invalid_rec).mdcvld_prodmap_ok:
                    invalid_prod_list.add(self.read(cr, uid, invalid_rec, 
                                                    [ordermap_rec[0].order_prod])[ordermap_rec[0].order_prod])
            if len(invalid_cust_list) != 0:
                log_msg = log_msg + "\n    Invalid customer : " + str(invalid_cust_list.pop())
            if len(invalid_prod_list) != 0:
                log_msg = log_msg + "\n    Invalid product(s) : "
                for x in invalid_prod_list:
                    log_msg = log_msg + ", " + str(x)

    # Construct list of invalid products
    invalid_prod_list = set()
    for rec in self.search(cr, uid, [('mdcvld_prodmap_ok','=',False)]):
        prod_value = self.read(cr, uid, rec, [prod_field[self._name]])[prod_field[self._name]]
        if prod_value not in invalid_prod_list:        
            invalid_prod_list.add(prod_value)

    log_msg = log_msg + "\n\nThere are " + str(len(invalid_prod_list)) + " unique invalid products:"
    for x in invalid_prod_list:
        log_msg = log_msg + "\n" + x    
    
    # Write process log
    processlog = self.pool.get('mdc.processlog')
    processlog_value = {"srce_model" : str(self._name),
                        "process_name" : "Validate",
                        "process_date" : datetime.now(),
                        "log" : log_msg}
    processlog_rec = processlog.create(cr, uid, processlog_value,context)
 
