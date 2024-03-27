from odoo import http
from odoo.http import request
from odoo import fields, http, _

# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter
from markupsafe import Markup

from odoo import conf, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR, AND

from datetime import datetime


from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from operator import itemgetter

from odoo import fields, http, _
from odoo.http import request
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.osv.expression import AND, OR

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.project.controllers.portal import ProjectCustomerPortal


import json 
class WebsiteController(http.Controller):

    @http.route('/employee_timesheet', auth='user', website=True)
    def index_shop(self, **kw):
            projects = request.env['project.project'].sudo().search([ ('message_partner_ids', 'in', [request.env.user.partner_id.id])])
            projects2 = request.env['project.project'].sudo().search([ ],limit=1)

            tasks = request.env['project.task'].sudo().search([])
            tmp = {
                'projects': projects,
                'tasks': tasks,
                'projects2':projects2,
                }
            return request.render('website_timesheet.employee_timesheet', tmp)

    @http.route('/submit_form', type='http', auth='user', website=True)
    def submit_form(self, **post):
        task_id = post.get('task_id')
        project_id = post.get('project_id')
        unit_amount = post.get('hours')
        user_id  = request.uid
        employee_id = request.env['hr.employee'].sudo().search([('user_id','=',user_id)]) 
        task = request.env['project.task'].sudo().search([('id','=',task_id)]) 
        task.write({'user_ids': [(4, user_id) ]  }) 
        time_obj = datetime.strptime(unit_amount, '%H:%M')
        total_minutes = time_obj.hour * 60 + time_obj.minute
        float_hours = total_minutes / 60.0
        request.env['account.analytic.line'].sudo().create({
            'date': post.get('date'),
            'employee_id': employee_id.id,
            'project_id': int(project_id),
            'task_id': int(task_id),
            'unit_amount':float_hours ,
            'name': post.get('des'),
        })
        return request.redirect('/employee_timesheet')

    @http.route('/get_task_options', type='http', auth='public', methods=['POST'], csrf=False)
    def get_task_options(self, project_id):
        options = []
        if project_id:
            tasks = request.env['project.task'].sudo().search([('project_id', '=', int(project_id))])
            assign_task = []
            for task in tasks:
                if request.env.user in task.user_ids:
                    assign_task.append(task)
            
            options = [{'id': task.id, 'name': task.name} for task in assign_task]
        print ("options  = ",options)
        return request.make_response(json.dumps(options), headers=[('Content-Type', 'application/json')])

class TimesheetCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'timesheet_count' in counters:
            Timesheet = request.env['account.analytic.line']
            employee_id = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

            domain = [('employee_id','=',employee_id.id)]
            values['timesheet_count'] = Timesheet.sudo().search_count(domain)
        return values

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none', **kw):
        Timesheet = request.env['account.analytic.line']
        employee_id = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)])

        domain = [('employee_id','=',employee_id.id)]
        print (">>>>>>>>>>>>>>>>>>>>>>>>= domain =",domain)
        Timesheet_sudo = Timesheet.sudo()

        values = self._prepare_portal_layout_values()
        _items_per_page = 100

        searchbar_sortings = self._get_searchbar_sortings()

        searchbar_inputs = self._get_searchbar_inputs()

        searchbar_groupby = self._get_searchbar_groupby()

        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [("date", "=", today)]},
            'week': {'label': _('This week'), 'domain': [('date', '>=', date_utils.start_of(today, "week")), ('date', '<=', date_utils.end_of(today, 'week'))]},
            'month': {'label': _('This month'), 'domain': [('date', '>=', date_utils.start_of(today, 'month')), ('date', '<=', date_utils.end_of(today, 'month'))]},
            'year': {'label': _('This year'), 'domain': [('date', '>=', date_utils.start_of(today, 'year')), ('date', '<=', date_utils.end_of(today, 'year'))]},
            'quarter': {'label': _('This Quarter'), 'domain': [('date', '>=', quarter_start), ('date', '<=', quarter_end)]},
            'last_week': {'label': _('Last week'), 'domain': [('date', '>=', date_utils.start_of(last_week, "week")), ('date', '<=', date_utils.end_of(last_week, 'week'))]},
            'last_month': {'label': _('Last month'), 'domain': [('date', '>=', date_utils.start_of(last_month, 'month')), ('date', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': _('Last year'), 'domain': [('date', '>=', date_utils.start_of(last_year, 'year')), ('date', '<=', date_utils.end_of(last_year, 'year'))]},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        timesheet_count = Timesheet_sudo.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/timesheets",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'filterby': filterby, 'groupby': groupby},
            total=timesheet_count,
            page=page,
            step=_items_per_page
        )

        def get_timesheets():
            groupby_mapping = self._get_groupby_mapping()
            field = groupby_mapping.get(groupby, None)
            orderby = '%s, %s' % (field, order) if field else order
            timesheets = Timesheet_sudo.search(domain, order=orderby, limit=_items_per_page, offset=pager['offset'])
            if field:
                if groupby == 'date':
                    raw_timesheets_group = Timesheet_sudo.read_group(
                        domain, ["unit_amount:sum", "ids:array_agg(id)"], ["date:day"]
                    )
                    grouped_timesheets = [(Timesheet_sudo.browse(group["ids"]), group["unit_amount"]) for group in raw_timesheets_group]

                else:
                    time_data = Timesheet_sudo.read_group(domain, [field, 'unit_amount:sum'], [field])
                    mapped_time = dict([(m[field][0] if m[field] else False, m['unit_amount']) for m in time_data])
                    grouped_timesheets = [(Timesheet_sudo.concat(*g), mapped_time[k.id]) for k, g in groupbyelem(timesheets, itemgetter(field))]
                return timesheets, grouped_timesheets

            grouped_timesheets = [(
                timesheets,
                sum(Timesheet_sudo.search(domain).mapped('unit_amount'))
            )] if timesheets else []
            return timesheets, grouped_timesheets

        timesheets, grouped_timesheets = get_timesheets()

        values.update({
            'timesheets': timesheets,
            'grouped_timesheets': grouped_timesheets,
            'page_name': 'timesheet',
            'default_url': '/my/timesheets',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'is_uom_day': request.env['account.analytic.line']._is_timesheet_encode_uom_day(),
        })
        return request.render("hr_timesheet.portal_my_timesheets", values)



class ProjectCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'project_count' in counters:
            values['project_count'] = request.env['project.project'].search_count([]) \
                if request.env['project.project'].check_access_rights('read', raise_exception=False) else 0
        if 'task_count' in counters:
            values['task_count'] = request.env['project.task'].search_count([('user_ids', 'in', request.env.user.id)]) \
                if request.env['project.task'].check_access_rights('read', raise_exception=False) else 0
        return values
        


    def _get_my_tasks_searchbar_filters(self, project_domain=None, task_domain=None):
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('user_ids', 'in', request.env.user.id)]},
        }

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].search(project_domain or [])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group(AND([[('project_id', 'not in', projects.ids)], task_domain or []]),
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })
        return searchbar_filters




    
    def _prepare_tasks_values(self, page, date_begin, date_end, sortby, search, search_in, groupby, url="/my/tasks", domain=None, su=False):
        values = self._prepare_portal_layout_values()

        Task = request.env['project.task']
        milestone_domain = AND([domain, [('allow_milestones', '=', 'True')]])
        milestones_allowed = Task.sudo().search_count(milestone_domain, limit=1) == 1
        searchbar_sortings = dict(sorted(self._task_get_searchbar_sortings(milestones_allowed).items(),
                                         key=lambda item: item[1]["sequence"]))
        searchbar_inputs = self._task_get_searchbar_inputs(milestones_allowed)
        searchbar_groupby = self._task_get_searchbar_groupby(milestones_allowed)

        if not domain:
            domain = []
        if not su and Task.check_access_rights('read'):
            domain = AND([domain, request.env['ir.rule']._compute_domain(Task._name, 'read')])
        Task_sudo = Task.sudo()

        # default sort by value
        domain += [('user_ids', 'in', request.env.user.id)]
        if not sortby or (sortby == 'milestone' and not milestones_allowed):
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default group by value
        if not groupby or (groupby == 'milestone' and not milestones_allowed):
            groupby = 'project'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search reset if needed
        if not milestones_allowed and search_in == 'milestone':
            search_in = 'all'
        # search
        if search and search_in:
            domain += self._task_get_search_domain(search_in, search)

        # content according to pager and archive selected
        order = self._task_get_order(order, groupby)

        def get_grouped_tasks(pager_offset):
            tasks = Task_sudo.search(domain, order=order, limit=self._items_per_page, offset=pager_offset)
            print(">>>>>>>>>>>>>>>>>>>> tasks ",tasks)
            print(">>>>>>>>>>>>>>>>>>>> domain ",domain)
            request.session['my_project_tasks_history' if url.startswith('/my/projects') else 'my_tasks_history'] = tasks.ids[:100]

            tasks_project_allow_milestone = tasks.filtered(lambda t: t.allow_milestones)
            tasks_no_milestone = tasks - tasks_project_allow_milestone

            groupby_mapping = self._task_get_groupby_mapping()
            group = groupby_mapping.get(groupby)
            if group:
                if group == 'milestone_id':
                    grouped_tasks = [Task_sudo.concat(*g) for k, g in groupbyelem(tasks_project_allow_milestone, itemgetter(group))]

                    if not grouped_tasks:
                        if tasks_no_milestone:
                            grouped_tasks = [tasks_no_milestone]
                    else:
                        if grouped_tasks[len(grouped_tasks) - 1][0].milestone_id and tasks_no_milestone:
                            grouped_tasks.append(tasks_no_milestone)
                        else:
                            grouped_tasks[len(grouped_tasks) - 1] |= tasks_no_milestone

                else:
                    grouped_tasks = [Task_sudo.concat(*g) for k, g in groupbyelem(tasks, itemgetter(group))]
            else:
                grouped_tasks = [tasks] if tasks else []

            task_states = dict(Task_sudo._fields['kanban_state']._description_selection(request.env))
            if sortby == 'status':
                if groupby == 'none' and grouped_tasks:
                    grouped_tasks[0] = grouped_tasks[0].sorted(lambda tasks: task_states.get(tasks.kanban_state))
                else:
                    grouped_tasks.sort(key=lambda tasks: task_states.get(tasks[0].kanban_state))
            return grouped_tasks
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': get_grouped_tasks,
            'allow_milestone': milestones_allowed,
            'page_name': 'task',
            'default_url': url,
            'task_url': 'tasks',
            'pager': {
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'groupby': groupby, 'search_in': search_in, 'search': search},
                "total": Task_sudo.search_count(domain),
                "page": page,
                "step": self._items_per_page
            },
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
        })
        return values