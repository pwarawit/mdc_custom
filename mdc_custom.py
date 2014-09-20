# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

#from openerp.osv import fields, osv
from osv import osv, fields
import time
#from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class mdc_raworder1(osv.osv):
    _name = 'mdc.raworder1'
    _description = 'MDC Raw Order - Format 1'
    _columns = {
    'validate_date': fields.date('Validation Date', required=False),
    'cust_map_ok': fields.boolean('Customer Mapping OK?', required=False),
    'prod_map_ok': fields.boolean('Product Mapping OK?', required=False),
    'validate_remark': fields.text('Validation Remark', required=False),
	'deptcode': fields.char('DeptCode',size=256, required=False),
	'podate': fields.char('PODate',size=256, required=False),
	'deliverydate': fields.char('DeliveryDate',size=256, required=False),
	'paymentterm': fields.char('PaymentTerm',size=256, required=False),
	'pono': fields.char('PONo',size=256, required=False),
	'eanshiptolocno': fields.char('EanShipToLocNo',size=256, required=False),
	'textbox13': fields.char('textbox13',size=256, required=False),
	'textbox14': fields.char('textbox14',size=256, required=False),
	'textbox16': fields.char('textbox16',size=256, required=False),
	'eancorplocno': fields.char('EanCorpLocNo',size=256, required=False),
	'textbox35': fields.char('textbox35',size=256, required=False),
	'textbox79': fields.char('textbox79',size=256, required=False),
	'vendorcode': fields.char('VendorCode',size=256, required=False),
	'textbox82': fields.char('textbox82',size=256, required=False),
	'textbox85': fields.char('textbox85',size=256, required=False),
	'lineitemno_1': fields.char('LineItemNo_1',size=256, required=False),
	'eanproductcode': fields.char('EanProductCode',size=256, required=False),
	'productdesc': fields.char('ProductDesc',size=256, required=False),
	'invendorproductcode': fields.char('InVendorProductCode',size=256, required=False),
	'textbox8': fields.char('textbox8',size=256, required=False),
	'fullpallet': fields.char('FullPallet',size=256, required=False),
	'ordermultiple': fields.char('OrderMultiple',size=256, required=False),
	'orderedqty': fields.char('OrderedQty',size=256, required=False),
	'totorder': fields.char('TotOrder',size=256, required=False),
	'unitprice': fields.char('UnitPrice',size=256, required=False),
	'grosscaseprice': fields.char('GrossCasePrice',size=256, required=False),
	'pctdisc1': fields.char('PctDisc1',size=256, required=False),
	'lineitemamt': fields.char('LineItemAmt',size=256, required=False),
	'textbox24': fields.char('textbox24',size=256, required=False),
	'textbox48': fields.char('textbox48',size=256, required=False),
	'textbox86': fields.char('textbox86',size=256, required=False),
	'amtdisc1': fields.char('AmtDisc1',size=256, required=False),
	'pctdisc1_2': fields.char('PctDisc1_2',size=256, required=False),
	'netamt': fields.char('NetAmt',size=256, required=False),
	'textbox17': fields.char('textbox17',size=256, required=False),
	'textbox22': fields.char('textbox22',size=256, required=False),
	'list4': fields.char('list4',size=256, required=False),
    }
    _defaults = {
        'validate_remark':"",
    }

    def validate(self, cr, uid, ids, context):

        def custmap_check(rawcustname):
            custmap = self.pool.get('mdc.custmap')
            custmap_search_criteria = [("srce_cust_name","like",rawcustname),("srce_model","=","mdc.raworder1")]
            #custmap_search_criteria = [("srce_model","=","mdc.raworder1")]
            custmap_id_list = custmap.search(cr, uid, custmap_search_criteria, context = context)
            return custmap_id_list

        # Read all the needed customer info into cust_list
        cust = self.pool.get('res.partner')
        cust_search_criteria = [("customer","=",True)]
        cust_id_list = cust.search(cr, uid, cust_search_criteria, context=context)
        cust_field_list = ['name']
        cust_list = cust.read(cr, uid, cust_id_list, cust_field_list, context)
        # Create list of names
        cust_name_list = []
        for i in cust_list:
            cust_name_list.append(i['name'])

        # Loop for each selected records
        for obj_id in context.get('active_ids'):
            
            timestamp = time.strftime("%d %b %Y %H:%M:%S")

            # Get current raw order record into rec object
            rec = self.browse(cr, uid, obj_id)

            resulttext = timestamp + "\n    Validating textbox13: " + rec.textbox13 + "\n"

            # Check if the rec.textbox13 exists in cust_list, return dict if found.
            if cust_name_list.count(rec.textbox13) == 1:
                self.write(cr, uid, obj_id, {"cust_map_ok":True}, context=context)
                resulttext = resulttext + "\n Customer Name FOUND!!! \n\n"
            else:
                resulttext = resulttext + "\n No matched with existing customer name -- checking with Customer Mapping Tables..."
                # Call function to check custmap 
                resulttext = resulttext + str(custmap_check(rec.textbox13))
                self.write(cr, uid, obj_id, {"cust_map_ok":False}, context=context)
                resulttext = resulttext + "\n Customer Name NOT FOUND!!! \n\n"

            # Compose validation result
            for i in cust_list:
                if i['name'] == rec.textbox13:
                    resulttext = resulttext + "\n" + i['name'] + " ----- " + str(i['name'] == rec.textbox13)

            resulttext = resulttext + "\n number of times matches: " + str(cust_name_list.count(rec.textbox13))

            self.write(cr, uid, obj_id, {"validate_date":timestamp, "validate_remark":resulttext}, context=context)

        return 


mdc_raworder1()

class mdc_cust_map(osv.osv):
    _name = 'mdc.custmap'
    _description = 'MDC Customer Mapping'
    _columns = {
    'srce_model' : fields.char('Source Model', size=32, required=True),
    'srce_cust_field' : fields.char('Source Customer Field', size=256, required=True),
    'srce_cust_value' : fields.char('Source Customer Value', size=256, required=True),
    'dest_cust_name' : fields.char('Destination Customer Name', size=256,
        required=True),
    }
mdc_cust_map()

class mdc_prod_map(osv.osv):
    _name = 'mdc.prodmap'
    _description = 'MDC Product Mapping'
    _columns = {
    'srce_model' : fields.char('Source Model', size=32, required=True),
    'srce_prod_field' : fields.char('Source Product Field', size=256, required=True),
    'srce_prod_value' : fields.char('Source Product Value', size=256, required=True),
    'dest_prod_name' : fields.char('Destination Product Name', size=256,
        required=True),
    }
    
    def update(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'srce_model':time.strftime("%d %b %Y %H:%M:%S")}, context=context) 
mdc_prod_map()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
