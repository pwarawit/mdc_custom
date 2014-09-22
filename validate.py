# -*- coding: utf-8 -*-
from osv import osv, fields
import time

def validate(self,srce, cr, uid, context):
    '''
        Validate Functions
        srce = Source Model - mdc.raworder1 | mdc.raworder2 | mdc.raworder3
    '''
    # Define dictionary for fieldnames
    cust_field = {"mdc.raworder1":"eanshiptolocno", 
                  "mdc.raworder2":"custname2", 
                  "mdc.raworder3":"custname3"}
    partner_search_field = {"mdc.raworder1":"ref",
                         "mdc.raworder2":"name",
                         "mdc.raworder3":"ref"}
    prod_field = {"mdc.raworder1":"", "mdc.raworder2":"custname2", "mdc.raworder3":"custname3"}
    
    # Loop through each records on srce
    for rec_id in self.search(cr, uid, []):
        # read customer value from raworder 
        cust_value =  self.read(cr, uid, rec_id,[cust_field[self._name]])[cust_field[self._name]]
        partner = self.pool.get('res.partner')
        print cust_value
        print partner_search_field[self._name]
        #search_str = "'" + partner_search_field[self._name] + "',"
        #print partner.search(cr, uid, [partner_search_field[self._name],'=',cust_value])
        '''
    print self
    print self.read(cr, uid, self.search(cr, uid,[]), ['podate'])
    raworder = self.pool.get(srce)
'''
    
'''
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
'''        