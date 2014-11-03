# -*- coding: utf-8 -*-
from osv import osv, fields
import time
import datetime
from openerp.osv import osv
from openerp.tools.translate import _
import validate
import convert
import create_lpout

class mdc_order_bigc(osv.osv):
    _name = 'mdc.order.bigc'
    _description = 'MDC Raw Order Big C'
    _columns = {
    'mdcvld_date' : fields.datetime('Validate Date', required=False),
    'mdcvld_ok' : fields.boolean('Validate OK?', required=False),
    'mdcvld_custmap_ok' : fields.boolean('Customer Valid?', required=False),
    'mdcvld_prodmap_ok' : fields.boolean('Product Valid?', required=False),
    'mdcvld_remark' : fields.text('Validation Remark', required=False),
    'mdcso_date' : fields.datetime('Convert Date', required=False),
    'mdcso_ok' : fields.boolean('Convert OK?', required=False),             
    'mdcso_customer' : fields.char('SO Customer ', required=False),
    'mdcso_cust_delivery' : fields.char('SO Delivery Customer', required=False),
    'mdcso_cust_invoice' : fields.char('SO Invoice Customer', required=False),
    'mdcso_orderdate' : fields.date('SO Order Date', required=False),
    'mdcso_deliverydate' : fields.date('SO Delivery Date', required=False),
    'mdcso_order_ref' : fields.char('SO Order Reference', size=256, required=False),
    'mdcso_prod_linenum' : fields.integer('SO Product Line Item number', required=False),
    'mdcso_prod_name' : fields.char('SO Product Line name', size=256, required=False),
    'mdcso_prod_qty' : fields.integer('SO Product Quantity', required=False),
    'mdcso_prod_price' : fields.float('SO Product Unit Price', required=False),
    'deptcode' : fields.char('deptcode', size=256, required=False),
    'podate' : fields.char('podate', size=256, required=False),
    'deliverydate' : fields.char('deliverydate', size=256, required=False),
    'paymentterm' : fields.char('paymentterm', size=256, required=False),
    'pono' : fields.char('pono', size=256, required=False),
    'eanshiptolocno' : fields.char('eanshiptolocno', size=256, required=False),
    'textbox13' : fields.char('textbox13', size=256, required=False),
    'textbox14' : fields.char('textbox14', size=256, required=False),
    'textbox16' : fields.char('textbox16', size=256, required=False),
    'eancorplocno' : fields.char('eancorplocno', size=256, required=False),
    'textbox35' : fields.char('textbox35', size=256, required=False),
    'textbox79' : fields.char('textbox79', size=256, required=False),
    'vendorcode' : fields.char('vendorcode', size=256, required=False),
    'textbox82' : fields.char('textbox82', size=256, required=False),
    'textbox85' : fields.char('textbox85', size=256, required=False),
    'lineitemno_1' : fields.char('lineitemno_1', size=256, required=False),
    'eanproductcode' : fields.char('eanproductcode', size=256, required=False),
    'productdesc' : fields.char('productdesc', size=256, required=False),
    'invendorproductcode' : fields.char('invendorproductcode', size=256, required=False),
    'textbox8' : fields.char('textbox8', size=256, required=False),
    'fullpallet' : fields.char('fullpallet', size=256, required=False),
    'ordermultiple' : fields.char('ordermultiple', size=256, required=False),
    'orderedqty' : fields.char('orderedqty', size=256, required=False),
    'totorder' : fields.char('totorder', size=256, required=False),
    'unitprice' : fields.char('unitprice', size=256, required=False),
    'grosscaseprice' : fields.char('grosscaseprice', size=256, required=False),
    'pctdisc1' : fields.char('pctdisc1', size=256, required=False),
    'lineitemamt' : fields.char('lineitemamt', size=256, required=False),
    'textbox24' : fields.char('textbox24', size=256, required=False),
    'textbox48' : fields.char('textbox48', size=256, required=False),
    'textbox86' : fields.char('textbox86', size=256, required=False),
    'amtdisc1' : fields.char('amtdisc1', size=256, required=False),
    'pctdisc1_2' : fields.char('pctdisc1_2', size=256, required=False),
    'netamt' : fields.char('netamt', size=256, required=False),
    'textbox17' : fields.char('textbox17', size=256, required=False),
    'textbox22' : fields.char('textbox22', size=256, required=False),
    'list4' : fields.char('list4', size=256, required=False),
    }

    def validate(self, cr, uid, ids, context):
        validate.validate(self, cr, uid, context)
        
    def convert(self, cr, uid, ids, context):
        convert.convert(self, cr, uid, context)       
mdc_order_bigc

class mdc_custmap(osv.osv):
    _name = 'mdc.custmap'
    _description = 'MDC Customer Mapping'
    _columns = {
    'srce_model' : fields.char('Source Model', size=32, required=False),
    'srce_cust_field' : fields.char('Source Customer Field', size=32, required=False),
    'srce_cust_value' : fields.char('Source Customer Value', size=256, required=False),
    'dest_cust_value' : fields.char('Destination Customer Value', size=256, required=False),
    }
mdc_custmap

class mdc_prodmap(osv.osv):
    _name = 'mdc.prodmap'
    _description = 'MDC Product Mapping'
    _columns = {
    'srce_model' : fields.char('Source Model', size=32, required=False),
    'srce_prod_field' : fields.char('Source Product Field', size=32, required=False),
    'srce_prod_value' : fields.char('Source Product Value', size=256, required=False),
    'dest_prod_field' : fields.char('Destination Product Field', size=256, required=False),
    'dest_prod_value' : fields.char('Destination Product Value', size=256, required=False),
    }
mdc_prodmap

class mdc_processlog(osv.osv):
    _name = 'mdc.processlog'
    _description = 'MDC Process Log'
    _columns = {
    'srce_model' : fields.char('Source Model', size=32, required=False),
    'process_name' : fields.char('Process Name', size=32, required=False),
    'process_date' : fields.datetime('Process Date', required=False),
    'log' : fields.text('Log Messages', required=False),
    }
    _order = 'process_date desc'
mdc_processlog

class sale_order(osv.osv):
    
    _inherit = "sale.order"
    
    _columns = {
        'date_expected': fields.date('Expected Delivery Date', required=False, readonly=False),
        'inv_ref' : fields.char('Ref.Invoice No', size=64),
        'delivery_zone': fields.selection([
        ('bangkok', 'Bangkok'),
        ('greater_bangkok', 'Greater Bangkok'),
        ('upcountry', 'Upcountry')],"Delivery Zone")        
        }
    _defaults = {
        'date_expected': lambda *a: datetime.datetime.now().strftime('%Y-%m-%d'),
        }
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context)
        part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        res['value'].update({'delivery_zone':part.delivery_zone})
        return res        
        
        
    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        # Overwrite with this date
        return order.date_expected
    
sale_order

class stock_picking(osv.osv):
  
    _inherit = "stock.picking"
    
    _columns = {
        'date_expected': fields.date('Expected Delivery Date', required=False, readonly=False),
        'inv_ref' : fields.char('Ref.Invoice No', size=64),
        'client_order_ref': fields.char('Customer Reference', size=64),
        'delivery_zone': fields.selection([
        ('bangkok', 'Bangkok'),
        ('greater_bangkok', 'Greater Bangkok'),
        ('upcountry', 'Upcountry')],"Delivery Zone")        
    }
    
stock_picking

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
            'delivery_zone': fields.selection([
            ('bangkok', 'Bangkok'),
            ('greater_bangkok', 'Greater Bangkok'),
            ('upcountry', 'Upcountry')],"Delivery Zone")
    }
res_partner

class stock_picking_out(osv.osv):
  
    _inherit = "stock.picking.out"
    
    _columns = {
        'date_expected': fields.date('Expected Delivery Date', required=False, readonly=False),
        'inv_ref' : fields.char('Ref.Invoice No', size=64),
        'client_order_ref': fields.char('Customer Reference', size=64),
    }
    
    def _prepare_order_picking(self, cr, uid, order, context=None):  
        vals = super(sale_order, self)._prepare_order_picking(cr, uid, order, context=context)
        vals.update({'date_expected': order.date_expected,
                     'inv_ref': order.inv_ref,
                     'client_order_ref': order.client_order_ref})
        return vals
  
    def create_lpout(self, cr, uid, ids, context):
        create_lpout.create_lpout(self, cr, uid, ids, 'bigc', context)
        
    def get_info_from_so(self, cr, uid, ids, context):
        # Find the Sale Order associate with the delivery order, and then copy 3 fields from SO to DO
        for id in ids:
            do_obj = self.browse(cr, uid, id, context=None)
            so_obj = self.pool.get('sale.order')
            so_id = so_obj.search(cr, uid, [('name','=',do_obj.origin)])
            so_rec = so_obj.browse(cr, uid, so_id , context=None)
            if so_rec:
                so_date_expected = so_rec[0].date_expected
                so_inv_ref = so_rec[0].inv_ref
                so_client_order_ref = so_rec[0].client_order_ref
                self.write(cr, uid, id, {'date_expected' : so_date_expected,
                                     'inv_ref' : so_inv_ref,
                                     'client_order_ref' : so_client_order_ref 
                                     },context=context)
        # WATCH OUT AND TO DO - write soem check if there is already existing values, do not overwrite it
  
stock_picking_out

class mdc_settings_lpout(osv.osv):
    _name = 'mdc.settings.lpout'
    _description = 'LP Output Creation Settings'
    _columns = {
    'name' : fields.char('Setting Name', size=64, required=True),
    'header' : fields.text('Column Header', required=False),
    'deliveryorder' : fields.char('Delivery Order Mapping', size=64, required=False),
    'doitem' : fields.integer('DO Item Steps', required=False),
    'material' : fields.char('Material Mapping', size=64, required=False),
    'materialdescription' : fields.char('Material Description Mapping', size=64, required=False),
    'salesunit' : fields.char('Sales Unit', size=64, required=False),
    'dateformat' : fields.char('Date Format', size=64, required=False),
    'timeformat' : fields.char('Time Format', size=64, required=False),
    'deliveryorderdate' : fields.char('Delivery Order Date Mapping', size=64, required=False),
    'createdby' : fields.char('Created by Mapping', size=64, required=False),
    'shiptoparty' : fields.char('Ship-To Party Mapping', size=64, required=False),
    'shiptoname' : fields.char('Ship-To Name Mapping', size=64, required=False),
    'street' : fields.char('Street Mapping', size=64, required=False),
    'street2' : fields.char('Street2 Mapping', size=64, required=False),
    'city' : fields.char('City Mapping', size=64, required=False),
    'postalcode' : fields.char('Postal Code Mapping', size=64, required=False),
    'salesorder' : fields.char('Sales Order Mapping', size=64, required=False),
    'salesorderitem' : fields.char('Sales Order Item Mapping', size=64, required=False),
    }
    _defaults = {
        'header':
        '''Delivery Order,DO Item,Material,Material Description,Delivery Qty,Sales Unit,Planned GI Date,Planned GI Time,Delivery Order Date,Created By,Ship-to Party,Ship-to Name,Street,Street2,Street3,City,Postal Code,Sales Order,Sales Order Item
        ''',
        'doitem' : 10
    }

mdc_settings_lpout

class mdc_ordermap(osv.osv):
    _name = 'mdc.ordermap'
    _description = 'MDC Raw Order Mapping'
    _columns = {
    'name' : fields.char('Mapping Name', size=64, required=True),
    'order_cust' : fields.char('Customer field in raw order', size=64, required=False),
    'order_cust_ship' : fields.char('Customer Shipping filed in raw order', size=64, required=False),
    'order_cust_inv' : fields.char('Customer Invoice field in raw order', size=64, required=False),
    'order_prod' : fields.char('Product field in raw order', size=64, required=False),
    'order_date' : fields.char('Order date field in raw order', size=64, required=False),
    'order_delivery_date' : fields.char('Delivery date field in raw order', size=64, required=False),
    'order_ref' : fields.char('Reference (PO Number) field', size=64, required=False),
    'order_line_num' : fields.char('Line number field ', size=64, required=False),
    'order_line_qty' : fields.char('Line quantity field', size=64, required=False),
    'order_line_price' : fields.char('Line product price field', size=64, required=False),
    'order_line_amt' : fields.char('Line amount field ', size=64, required=False),
    'order_total_amt' : fields.char('Total order amount field', size=64, required=False),
    'map_cust' : fields.char('Customer Map field', size=64, required=False),
    'map_cust_ship' : fields.char('Customer Shipping Map field', size=64, required=False),
    'map_cust_inv' : fields.char('Customer Invoice Map field', size=64, required=False),
    'map_prod' : fields.char('Product Map field', size=64, required=False),
    'key_cust' : fields.char('Key Customer field', size=64, required=False),
    'key_cust_ship' : fields.char('Key Customer Shipping field', size=64, required=False),
    'key_cust_inv' : fields.char('Key Customer Invoice field', size=64, required=False),
    'key_prod' : fields.char('Key Product field', size=64, required=False),
    }
    _order = 'name'

mdc_ordermap

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
