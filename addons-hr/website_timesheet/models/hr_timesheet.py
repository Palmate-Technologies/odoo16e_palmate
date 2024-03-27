# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from lxml import etree
import re

from odoo import api, Command, fields, models, _, _lt
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.osv import expression

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'



  #  def _timesheet_get_portal_domain(self):
   #     if self.env.user.has_group('hr_timesheet.group_hr_timesheet_user'):
            # Then, he is internal user, and we take the domain for this current user
       #     return self.env['ir.rule']._compute_domain(self._name)
#
     #   return [ ('task_id.user_ids', 'in', self.env.user.id) ]

    