# -*- coding: utf-8 -*-

from osv import osv, fields
import time
from datetime import datetime

def create_lpout(self, cr, uid, setting_name, context=None):
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
    
    # Write process log
    processlog = self.pool.get('mdc.processlog')
    processlog_value = {"srce_model" : str(self._name),
                        "process_name" : "Create LP OUT",
                        "process_date" : datetime.now(),
                        "log" : log_msg}
    processlog_rec = processlog.create(cr, uid, processlog_value,context)    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
