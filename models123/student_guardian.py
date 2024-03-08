# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
# from odoo.exceptions import Warning, UserError
from odoo.exceptions import UserError

class Studentguardian(models.Model):
    
    _name = 'student.guardian'
    _description = 'Student guardian '
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']      # odoo11
    _order = 'id desc'
    
    # def unlink(self):
    #     for rec in self:
    #         if rec.state not in ('draft', 'in_active', 'blocked'):
    #             raise UserError(_('You can not delete Student guardian which is not in draft or cancelled or blocked state.'))
    #     return super(Studentguardian, self).unlink()
    
    sub_guardian_ids = fields.One2many('student.guardian','sub_guardian_id',string='Sub Guardians')
    sub_guardian_id = fields.Many2one('student.guardian',string='Sub Guardian')
    number = fields.Char(string='Family Number',  index=True, readonly=True, tracking=True )
    name = fields.Char(string="Father Name", index=True, tracking=True )
    state = fields.Selection([
        ('draft', 'New'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('in_active', 'In Active'),
        ],
        default='draft',
        srting="Family State",
        tracking=True
    )

    active = fields.Boolean(default=True)
    gender = fields.Many2one('gender', required=True, copy=True, tracking=True)
    nationality = fields.Many2one('res.country', required=True, copy=True, tracking=True)
    id_type = fields.Many2one('id.type', required=True, copy=True, tracking=True)
    id_number = fields.Char('ID Number', required=True, copy=True, tracking=True)
    active =fields.Boolean(default=True)
    gender = fields.Many2one('gender', required=True, copy=True,  tracking=True,)
    nationality = fields.Many2one('res.country', required=True, copy=True,  tracking=True,)
    id_type = fields.Many2one('id.type', required=True, copy=True,  tracking=True,)
    id_number = fields.Char('Id Number', required=True, copy=True,  tracking=True,)
    tage = fields.Many2one('res.partner.category', required=True, copy=True,  tracking=True,)
    know_us = fields.Many2one('know.us', required=True, copy=True,  tracking=True,)
    work_type = fields.Many2one('work.type', required=True, copy=True,  tracking=True,)
    work_source = fields.Char('Work Source', required=True, copy=True,  tracking=True,)
    partner_id = fields.Many2one('res.partner', required=True, copy=True,  tracking=True,)
    mobile = fields.Char('Mobile', required=True, copy=True, tracking=True,)
    mobile2 = fields.Char('Mobile2', required=True, copy=True,  tracking=True,)
    job_position = fields.Char('Job Position',  required=True, copy=True, tracking=True,)
    email = fields.Char('Email',  required=True,  copy=True,  tracking=True,)
    student_ids = fields.One2many('student.student','guardian_id',string='Students')
    # sub_guardian_ids = fields.One2many('student.guardian','sub_guardian_id',string='Sub Guardians')
    sub_guardian_id = fields.Many2one('student.guardian',string='Sub Guardian')
    guardian_date = fields.Date(string='Guardian Date', default=fields.Date.today(), required=True, copy=True, tracking=True, )
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id, required=True, copy=True, )
    date_end = fields.Date( string='guardian Deadline', readonly=True, help='Last date for the guardian to be needed', copy=True,)
    date_done = fields.Date( string='Date Done', readonly=True,  help='Date of Completion of guardian Student', )      
    confirm_date = fields.Date( string='Confirmed Date', readonly=True,copy=False,)
    userblocked_date = fields.Date(  string='Blocked Date',  readonly=True, copy=False, )
    employee_confirm_id = fields.Many2one('hr.employee', string='Confirmed by',  readonly=True,copy=False, )
    blocked_employee_id = fields.Many2one('hr.employee', string='Blocked by',  readonly=True,copy=False, )

    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for guardian in self:
            guardian.student_count = len(guardian.student_ids)

    # student_ids is a One2many or Many2many field that references students related to the guardian
    # Add the rest of your fields and methods here

    
# seq 
    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('student.guardian.seq') or _('New')
        res = super(Studentguardian, self).create(vals)
        return res
    
    def family_confirm(self):
        for rec in self:
            # manager_mail_template = self.env.ref('reg.email_confirm_school_reg_base')
            rec.employee_confirm_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.confirm_date = fields.Date.today()
            rec.state = 'active'
            # if manager_mail_template:
            #     manager_mail_template.send_mail(self.id)
            
    def family_blocked(self):
        for rec in self:
            rec.state = 'blocked'
            rec.blocked_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.userblocked_date = fields.Date.today()

    def reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_archive(self):
        for rec in self:
            rec.active= False


