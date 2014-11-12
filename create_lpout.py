# -*- coding: utf-8 -*-

from osv import osv, fields
import time
from datetime import datetime

def create_lpout(self, cr, uid, ids, setting_name, context=None):
    '''
        Create LP OUT file function - This function will create CSV string from selected stock.picking.out records
        for uploading to LP (3rd party logistics). It will rconvert from raw order to Sale Order
        self = Self Model - mdc.order.bigc | mdc.order.lotus| mdc.order.robinson
        settings = name of the mdc.settings.lpout record to be used.
    '''
    timestamp = time.strftime("%d %b %Y %H:%M:%S")
    log_msg = timestamp + "\nCreation of LP OUT File using setting : " + str(setting_name) + " started...\n=================\n\n"
    
    setting_obj = self.pool.get('mdc.settings.lpout')
    setting = setting_obj.browse(cr, uid, setting_obj.search(cr, uid, [('name','=',str(setting_name))]), context)
    log_msg = log_msg + setting[0].header
    
    # Read all the product and customer info needed
    products = self.pool.get('product.product')
    all_prod = products.read(cr, uid, products.search(cr, uid, [('active', '=', True)]),
                                 ['id', 'code', 'ean13', 'name.template', 'default_code','name'])
    customers = self.pool.get('res.partner')
    all_custs = customers.read(cr, uid, customers.search(cr, uid, [('active', '=', True),('customer','=', True)]),
                                 ['id', 'name','ean13','street','street2','zip', 'city', 'ref'])
    
    line_count = 0
    # Loop for each id in ids (each stock.picking.out selected)
    for id in ids:
        # Browse each record of Delivery Order (do_rec) 
        do_rec = self.pool.get('stock.picking.out').read(cr, uid, id, context=context)
        
        # Find customer
        cust_id = do_rec['partner_id'][0]
        ship_to_party = ''
        ship_to_name = ''
        street = ''
        street2 = ''
        city = ''
        postalcode = ''
        for cust in all_custs:
            if cust['id'] == cust_id:
                if setting[0].shiptoparty:
                    ship_to_party = cust[setting[0].shiptoparty]
                if setting[0].shiptoname:
                    ship_to_name = cust[setting[0].shiptoname]
                if setting[0].street:
                    street = cust[setting[0].street]
                if setting[0].street2:
                    street2 = cust[setting[0].street2]
                if setting[0].city:
                    city = cust[setting[0].city]                
                if setting[0].postalcode:
                    postalcode = cust[setting[0].postalcode]
                break
        # Find each stock move line
        stock_move_obj = self.pool.get('stock.move')
        do_lines = stock_move_obj.read(cr, uid, stock_move_obj.search(cr, uid, [('picking_id','=',do_rec['id'])]), context=context)
        
        for do_line in do_lines:
            # Compose string for each line
            line_count = line_count + 1
            
            if not do_rec[setting[0].deliveryorder]:
                raise osv.except_osv('Error',    'Customer Reference can not be blank.')
            if not do_rec[setting[0].deliveryorderdate]:
                raise osv.except_osv('Error',    'Expected Delivery Date can not be blank.')
            
            log_msg = log_msg + "\n" + do_rec[setting[0].deliveryorder]
            log_msg = log_msg + "," + str(line_count * setting[0].doitem)
            # Get the prod_id from stock_move record
            prod_id = do_line['product_id'][0]
            # Searching product from all_prod list
            prod_code_val = ''
            prod_desc_val = ''
            for prod in all_prod:
                if prod['id'] == prod_id:
                    prod_code_val = prod[setting[0].material]
                    prod_desc_val = prod[setting[0].materialdescription]
                    break
            log_msg = log_msg + "," + prod_code_val + "," + prod_desc_val
            log_msg = log_msg + "," + str(int(do_line['product_qty']))
            log_msg = log_msg + "," + setting[0].salesunit
            log_msg = log_msg + "," + time.strftime(setting[0].dateformat)
            log_msg = log_msg + "," + time.strftime(setting[0].timeformat)
            log_msg = log_msg + "," + datetime.strptime(do_rec[setting[0].deliveryorderdate],'%Y-%m-%d').strftime(setting[0].dateformat)
            log_msg = log_msg + "," + setting[0].createdby
            log_msg = log_msg + "," + ship_to_party
            log_msg = log_msg + "," + ship_to_name
            log_msg = log_msg + "," + street
            log_msg = log_msg + "," + street2
            # skip street3 - always
            log_msg = log_msg + ",," + city
            log_msg = log_msg + "," + postalcode
            log_msg = log_msg + "," + setting[0].salesorder
            log_msg = log_msg + "," + setting[0].salesorderitem
            
    
    # Write process log
    processlog = self.pool.get('mdc.processlog')
    processlog_value = {"srce_model" : str(self._name),
                        "process_name" : "Create LP OUT",
                        "process_date" : datetime.now(),
                        "log" : log_msg}
    processlog_rec = processlog.create(cr, uid, processlog_value,context)    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
