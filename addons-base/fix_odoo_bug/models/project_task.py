# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class Task(models.Model):
    _inherit = 'project.task'

    is_timeoff_task = fields.Boolean("Is Time off Task", compute="_compute_is_timeoff_task", search="_search_is_timeoff_task_new")

    def _search_is_timeoff_task_new(self, operator, value):
        if operator not in ['=', '!='] or not isinstance(value, bool):
            raise NotImplementedError(_('Operation not supported'))
        leave_type_read_group = self.env['hr.leave.type']._read_group(
            [('timesheet_task_id', '!=', False)],
            ['timesheet_task_ids:array_agg(timesheet_task_id)'],
            [],
        )
        timeoff_task_ids = leave_type_read_group[0]['timesheet_task_ids'] if leave_type_read_group else []
        if self.env.company.leave_timesheet_task_id:
            timeoff_task_ids.append(self.env.company.leave_timesheet_task_id.id)
        if operator == '!=':
            value = not value
        return [('id', 'in' if value else 'not in', timeoff_task_ids)]


