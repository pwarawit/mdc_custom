# -*- coding: utf-8 -*-

from osv import osv, fields
import time
import datetime

class mdc_settings_lpout(osv.osv):
    _name = 'mdc.settings.lpout'
    _description = 'LP Output Creation Settings'
    _columns = {
    'name' : fields.char('Setting Name', size=64, required=True),
    'header' : fields.text('Column Header', required=False),
    'field1' : fields.char('field1', size=256, required=False),
    'field2' : fields.char('field2', size=256, required=False),
    'field3' : fields.char('field3', size=256, required=False),
    'field4' : fields.char('field4', size=256, required=False),
    'field5' : fields.char('field5', size=256, required=False),
    'field6' : fields.char('field6', size=256, required=False),
    'field7' : fields.char('field7', size=256, required=False),
    'field8' : fields.char('field8', size=256, required=False),
    'field9' : fields.char('field9', size=256, required=False),
    'field10' : fields.char('field10', size=256, required=False),
    'field11' : fields.char('field11', size=256, required=False),
    }

mdc_settings_lpout()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
