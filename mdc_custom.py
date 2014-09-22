# -*- coding: utf-8 -*-
from osv import osv, fields
import time

class mdc_raworder1(osv.osv):
    _name = 'mdc.raworder1'
    _description = 'MDC Raw Order Format 1 (Big C)'
    _columns = {
    'mdcvld_date' : fields.date('Validation Date', required=False),
    'mdcvld_ok' : fields.boolean('Validation overall OK?', required=False),
    'mdcvld_custmap_ok' : fields.boolean('Customer Mapping OK?', required=False),
    'mdcvld_prodmap_ok' : fields.boolean('Product Mapping OK?', required=False),
    'mdcvld_remark' : fields.text('Validation Remark', required=False),
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
mdc_raworder1


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
