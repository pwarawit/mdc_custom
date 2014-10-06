# -*- coding: utf-8 -*-
from osv import osv, fields
import time
from datetime import datetime

def convert(self, cr, uid, context):
    '''
        Convert Functions - convert from raw order to Sale Order
        self = Self Model - mdc.order.bigc | mdc.order.lotus| mdc.order.robinson
    '''
    partner_search_field = {"mdc.order.bigc":"name",
                         "mdc.order.lotus":"name",
                         "mdc.order.robinson":"ref"}
    
    prod_field = {"mdc.order.bigc":"ean13",
                  "mdc.order.lotus":"ean13",
                  "mdc.order.robinson":"ean13"}
    
    # Hardcoded default values
    pricelist_id = 1
    tax_id = [2] #Output VAT
    
    timestamp = time.strftime("%d %b %Y %H:%M:%S")
    log_msg = timestamp + "\nConvert from raw order(" + str(self._name) + ") to Sales Order started...\n"
    
    # Construct the set of POs (use set instead of list to prevent duplication)
    po_list = set()
    for rec_id in self.search(cr, uid, []):
        # create object for current record
        rec_obj = self.browse(cr, uid, rec_id, context)
        if rec_obj.mdcvld_ok and not rec_obj.mdcso_ok:
            # adding order reference into po_list 
            if rec_obj.mdcso_order_ref not in po_list:
                po_list.add(rec_obj.mdcso_order_ref)

    log_msg = log_msg + "\nThere will be " + str(len(po_list)) + " sale order(s) to be created.\n"
                
    # Loop through each of the POs
    for po_rec in po_list:
        # log_msg = log_msg + "\nCreating PO number : " + po_rec
        domain_criteria = [('mdcso_order_ref','=',po_rec)]
        # Read data and construct poline_list which get all records as list of each po line
        poline_list = self.read(cr, uid, self.search(cr, uid, domain_criteria),
                          ['id', 'mdcso_customer', 'mdcso_cust_delivery', 'mdcso_cust_invoice',
                           'mdcso_orderdate', 'mdcso_deliverydate','mdcso_order_ref',
                           'mdcso_prod_linenum','mdcso_prod_name', 'mdcso_prod_qty','mdcso_prod_price'])
        
        
        # Search customer for mdcso_customer name
        partner = self.pool.get('res.partner')
        partner_id = partner.search(cr, uid, [('name','=',poline_list[0]["mdcso_customer"])])

        # Construct so_value, dictionary that contains Sales Order value
        so_value = {"partner_id" : partner_id[0],
                    "partner_invoice_id" : partner_id[0],
                    "partner_shipping_id" : partner_id[0],
                    "pricelist_id" : pricelist_id,
                    "state" : "draft",
                    "client_order_ref" : poline_list[0]["mdcso_order_ref"],
                    "date_order" : poline_list[0]["mdcso_orderdate"],
                    "date_expected" : poline_list[0]["mdcso_deliverydate"]}
        
        # log_msg = log_msg + "\n" + str(so_value) + "\n"        
        log_msg = log_msg + "\n  PO: " + po_rec + " contains " + str(len(poline_list)) + " lines."
        
        # Create Sale Order
        so = self.pool.get('sale.order')
        so_rec = so.create(cr, uid, so_value, context)
        
        # Loop through each of the Order Lines
        for poline in poline_list:
            # Search product id from product table
            prod = self.pool.get('product.product')
            prod_id = prod.search(cr, uid, [(prod_field[self._name],'=',poline["mdcso_prod_name"])])
            prod_name = prod.read(cr, uid, prod_id[0], ['name']) 

            # Construct Sale Order Line, hard coded Tax to '2' - Output vat, and add 7% into price_unit 
            soline_value = {"order_id" : so_rec,
                            "name" : prod_name['name'],
                            "sequence" : poline['mdcso_prod_linenum'],
                            "product_id" : prod_id[0],
                            "price_unit" : poline['mdcso_prod_price'] * 1.07,
                            "tax_id" : [(6, 0, tax_id)],
                            "product_uom_qty" : poline['mdcso_prod_qty']
                            }
            soline = self.pool.get('sale.order.line')
            soline_rec = soline.create(cr, uid, soline_value, context)
            # log_msg = log_msg + "\n" + str(soline_value)
            
            # Write back to the raw order table mdcso_date, mdcso_ok
            self.write(cr, uid, poline['id'], {"mdcso_date" : timestamp,"mdcso_ok" : True} , context)
        
    # Write process log
    processlog = self.pool.get('mdc.processlog')
    processlog_value = {"srce_model" : str(self._name),
                        "process_name" : "Convert",
                        "process_date" : datetime.now(),
                        "log" : log_msg}
    processlog_rec = processlog.create(cr, uid, processlog_value,context)
