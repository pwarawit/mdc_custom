# -*- coding: utf-8 -*-
from osv import osv, fields
import time
from datetime import datetime

def convert(self, cr, uid, context):
    '''
        Convert Functions - convert from raw order to Sale Order
        self = Self Model - mdc.raworder1 | mdc.raworder2 | mdc.raworder3
    '''
    partner_search_field = {"mdc.raworder1":"name",
                         "mdc.raworder2":"name",
                         "mdc.raworder3":"ref"}
    
    prod_field = {"mdc.raworder1":"eanproductcode",
                  "mdc.raworder2":"custname2",
                  "mdc.raworder3":"custname3"}
    
    # Hardcoded default values
    pricelist_id = 1
    
    timestamp = time.strftime("%d %b %Y %H:%M:%S")
    log_msg = "\n" + timestamp + " Construct list of POs\n"
    
    # Construct the set of POs (use set instead of list to prevent duplication)
    po_list = set()
    for rec_id in self.search(cr, uid, []):
        # create object for current record
        rec_obj = self.browse(cr, uid, rec_id, context)
        if rec_obj.mdcvld_ok:
            # adding order reference into po_list 
            if rec_obj.mdcso_order_ref not in po_list:
                po_list.add(rec_obj.mdcso_order_ref)
            
    # Loop through each of the POs
    for po_rec in po_list:
        log_msg = log_msg + "\nCreating PO number : " + po_rec
        domain_criteria = [('mdcso_order_ref','=',po_rec)]
        # Read data and construct poline_list which get all records as list of each po line
        poline_list = self.read(cr, uid, self.search(cr, uid, domain_criteria),
                          ['id', 'mdcso_customer', 'mdcso_cust_delivery', 'mdcso_cust_invoice',
                           'mdcso_orderdate', 'mdcso_deliverydate','mdcso_order_ref',
                           'mdcso_prod_linenum','mdcso_prod_name', 'mdcso_prod_qty','mdcso_prod_price'])
        
        # Search customer for mdcso_customer name
        partner = self.pool.get('res.partner')
        partner_id = partner.search(cr, uid, [('name','=',poline_list[0]["mdcso_customer"])])
        print partner_id

        # Construct so_value, dictionary that contains Sales Order value
        so_value = {"partner_id" : partner_id[0],
                    "partner_invoice_id" : partner_id[0],
                    "partner_shipping_id" : partner_id[0],
                    "pricelist_id" : 1,
                    "state" : "progress",
                    "origin" : poline_list[0]["mdcso_order_ref"]}
        
        print "\n\n"
        print so_value
        #print poline_list[:]['mdcso_customer']
        print poline_list 
        
        log_msg = log_msg + "\n  PO: " + po_rec + " contains " + str(len(poline_list)) + " lines.\n"
        
        # Create Sale Order
        so = self.pool.get('sale.order')
        #so_rec = so.create(cr, uid, so_value, context)
        
        # Create Sale Order Line
        soline_value = {"order_id" : 22,
                        "name" : "testing order line",
                        "sequence" : 1,
                        "product_id" : 1,
                        "price_unit" : 0.5,
                        "product_uom_qty" : 5
                        }
        soline = self.pool.get('sale.order.line')
        soline_rec = soline.create(cr, uid, soline_value, context)
        
        #log_msg = log_msg + "\n  Sale Order ID: " + str(so_rec) + " created.\n\n"
        log_msg = log_msg + "\n  Sale Order ID: " + str(soline_rec) + " created.\n\n"
        
    print log_msg
        #print dicts
    
    #print po_list
    
#     partner = self.pool.get('res.partner')
#     raworder = self.search()
#     partner_object = partner.read(cr, uid, partner.search(cr, uid, [(partner_search_field[self._name], '=', self.mdcso_customer)]), ['id', 'name', 'ref'])
#     partner_id = partner_object['id']
#     print partner_id
    
    # Loop through each of the POs (Order Ref)
#     so = self.pool.get('sale.order')
#     so_value = {"partner_id" : 6,
#                 "partner_invoice_id" : 6,
#                 "partner_shipping_id" : 6,
#                 "pricelist_id" : 1}
#     so_rec = so.create(cr, uid, so_value, context)
#     print so_rec

#     # Read all data from res.partner and mdc_custmap
#     partner = self.pool.get('res.partner')
#     custmap = self.pool.get('mdc.custmap')
#     products = self.pool.get('product.product')
#     prodmap = self.pool.get('mdc.prodmap')
#     all_cust = partner.read(cr, uid, partner.search(cr, uid, [('customer', '=', True)]), ['id', 'name', 'ref'])
#     all_prod = products.read(cr, uid, products.search(cr, uid, [('active', '=', True)]), ['id', 'code', 'ean13', 'name.template'])
#     all_custmap = custmap.read(cr, uid, custmap.search(cr, uid, [('srce_model', '=', self._name)]),
#                                ['srce_cust_field', 'srce_cust_value', 'dest_cust_value'])
#     all_prodmap = prodmap.read(cr, uid, prodmap.search(cr, uid, [('srce_model', '=', self._name)]),
#                                ['srce_prod_field', 'srce_prod_value', 'dest_prod_value'])
#             
#     # Loop through each records on self
#     for rec_id in self.search(cr, uid, []):
#         # Initialize variables for this specific source records
#         custmap_ok = False
#         prodmap_ok = False
#         mdcso_cust = ""
#         mdcso_prod = ""
#         validate_all_ok = False
#         vldn_msg = timestamp + " Start Validating Customer..."
#         
#         # read customer & product value from raworder 
#         cust_value = self.read(cr, uid, rec_id, [cust_field[self._name]])[cust_field[self._name]]
#         prod_value = self.read(cr, uid, rec_id, [prod_field[self._name]])[prod_field[self._name]]
#         
#         
#         # Check with all_cust if matched
#         custmap_ok = False
#         for cust_rec in all_cust:
#             if custmap_ok:
#                 # If the customer has been found in earlier loop, then break
#                 break
#             if cust_rec[partner_search_field[self._name]] == cust_value:
#                 vldn_msg = vldn_msg + "\nRaw Customer Value: " + cust_value + "  matched with " + \
#                     cust_rec[partner_search_field[self._name]]
#                 mdcso_cust = cust_rec[partner_search_field[self._name]]
#                 custmap_ok = True
#                 break
#             else:
#                 # Check against all_custmap
#                 for custmap_rec in all_custmap:
#                     if (custmap_rec['srce_cust_field'] == partner_search_field[self._name]) and \
#                         (custmap_rec['srce_cust_value'] == cust_value):
#                         vldn_msg = vldn_msg + "\nRaw Customer Value: " + cust_value + "  matched with " + \
#                             custmap_rec['dest_cust_value'] + " via Customer Mappping Table."
#                         mdcso_cust = custmap_rec['dest_cust_value']
#                         custmap_ok = True
#                         break
#                     else:
#                         continue
#                         
#         if not custmap_ok: 
#             mdcso_cust = ""
#             vldn_msg = vldn_msg + "\n" + cust_value + " is INVALID CUSTOMER VALUE !!!"
#         
#         # Check with all_prod if matched
#         prodmap_ok = False
#         for prod_rec in all_prod:
#             if prodmap_ok:
#                 # If the product has been found in earlier loop, then break
#                 break
#             if prod_rec[product_search_field[self._name]] == prod_value:
#                 vldn_msg = vldn_msg + "\nRaw Product code: " + prod_value + " macthed with " + \
#                     prod_rec[product_search_field[self._name]]
#                 mdcso_prod = prod_rec[product_search_field[self._name]]
#                 prodmap_ok = True
#                 break
#             else:
#                 # Check against all_prodmap
#                 for prodmap_rec in all_prodmap:
#                     if (prodmap_rec['srce_prod_field'] == product_search_field[self._name]) and \
#                         (prodmap_rec['srce_prod_value'] == prod_value):
#                         vldn_msg = vldn_msg + "\nRaw Product Value: " + prod_value + " matched with " + \
#                             prodmap_rec['dest_prod_value'] + " via Product Mapping Table."
#                         mdcso_prod = prodmap_rec['dest_prod_value']
#                         prodmap_ok = True
#                         break
#                     else:
#                         continue
#         
#         if not prodmap_ok:
#             mdcso_prod = ""
#             vldn_msg = vldn_msg + "\n" + prod_value + " is INVALID PRODUCT VALUE!!!"
#         
#         if custmap_ok and prodmap_ok:
#             mdcvld_ok = True
#             # Read other fields data
#             cur_rec = self.read(cr, uid, rec_id, [
#                                         orderdate_field[self._name],
#                                         deliverydate_field[self._name],
#                                         orderref_field[self._name],
#                                         linenum_field[self._name],
#                                         prodqty_field[self._name],
#                                         prodprice_field[self._name]
#                                         ])
# 
#             # assume orderdate and delivery date format as for Big C
#             mdcso_orderdate = time.mktime(time.strptime(cur_rec[orderdate_field[self._name]][0:10],"%d/%m/%Y"))
#             mdcso_deliverydate = time.mktime(time.strptime(cur_rec[deliverydate_field[self._name]][0:10],"%d/%m/%Y"))
#             mdcso_orderdate = datetime.fromtimestamp(mdcso_orderdate)
#             mdcso_deliverydate = datetime.fromtimestamp(mdcso_deliverydate)
# 
#             self.write(cr, uid, rec_id, {
#                                      "mdcso_orderdate" : mdcso_orderdate,
#                                      "mdcso_deliverydate" : mdcso_deliverydate,
#                                      "mdcso_order_ref" : cur_rec[orderref_field[self._name]],
#                                      "mdcso_prod_linenum" : cur_rec[linenum_field[self._name]],
#                                      "mdcso_prod_qty" : int(float(cur_rec[prodqty_field[self._name]])),
#                                      "mdcso_prod_price" : float(cur_rec[prodprice_field[self._name]])
#                                      } , context)
#             #print curr_rec.orderref_field[self._name]
#             vldn_msg = vldn_msg + "\n\n Both customer and product valided successfully. Other fields populated"
#         else:
#             mdcvld_ok = False
#             
#         # Write the result of customer validation
#         self.write(cr, uid, rec_id, {"mdcvld_date" : timestamp,
#                                      "mdcvld_custmap_ok" : custmap_ok,
#                                      "mdcvld_prodmap_ok" : prodmap_ok,
#                                      "mdcvld_ok" : mdcvld_ok,
#                                      "mdcso_customer" : mdcso_cust,
#                                      "mdcso_cust_delivery" : mdcso_cust,
#                                      "mdcso_cust_invoice" : mdcso_cust,
#                                      "mdcso_prod_name" : mdcso_prod,
#                                      "mdcvld_remark" : vldn_msg,                                  
#                                      } , context)
# 
# # ToDO
# # Keep all the Write overall log into mdc_processlog table        
