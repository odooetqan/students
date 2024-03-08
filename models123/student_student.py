# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
# from odoo.exceptions import Warning, UserError
from odoo.exceptions import UserError

    
class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Students Model'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'id desc'

    number = fields.Char( string='Student Number',index=True, readonly=True, tracking=True, Default='NEW'  )
    family_number = fields.Char(related='guardian_id.number')
    family_name = fields.Char(related='guardian_id.name')
    name2 = fields.Char( string='Student Number.',index=True, readonly=True, tracking=True, Default='NEW', compute="student_name2"  )
    number2 = fields.Char( string='Number',index=True, readonly=True, tracking=True, Default='NEW', compute="student_name2"  )
    name = fields.Char( string='Student Name',index=True, tracking=True  )
    state = fields.Selection([
        ('draft', 'New'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('in_active', 'In Active'),
    ], default='draft', string="Student State", tracking=True)

    class_id = fields.Many2one("classes", string="Education Class", required=True, copy=True)
    stage_id = fields.Many2one("stages", string="Stage", related="class_id.stage_id", tracking=True, required=True)
    section_id = fields.Many2one("sections", string="Section", related="class_id.section_id", tracking=True, required=True)
    track_id = fields.Many2one("tracks", string="Track", tracking=True, related="class_id.track_id", required=True)
    secondary_major = fields.Many2one('secondry.majors', string='Secondary Major', tracking=True)
    ex_school = fields.Many2one('ex.schools', string='Ex School', required=True,  copy=True)
    current_year = fields.Many2one('years', string='Current Year', copy=True)
    previous_year = fields.Many2one('years', string='Previous Year', required=True,  copy=True)

    active = fields.Boolean(default=True)
    gender = fields.Many2one('gender', string='Gender', required=True, copy=True, tracking=True)
    nationality = fields.Many2one('res.country', string='Nationality', required=True, copy=True, tracking=True)
    id_type = fields.Many2one('id.type', string='ID Type', required=True, copy=True, tracking=True)
    id_number = fields.Char(string='ID Number', required=True, copy=True, tracking=True)
    tage = fields.Many2one('res.partner.category', string='Tage', required=True, copy=True, tracking=True)
    birth_date = fields.Date(string='Birth Date')
    hijri_date = fields.Date(string='Hijri Date')
    reason = fields.Many2one('dropoff.reasons', string='Reason')
    sibling_discount = fields.Many2one('discount.type', string='Sibling Discount')
    student_discount = fields.Many2one('discounts', string='Student Discount')

    qutetions_ids = fields.One2many('sale.order', 'partner_id')
    invoice_line_ids = fields.One2many('account.move.line', 'partner_id')
    invoice_ids = fields.One2many('account.move', 'partner_id')

    sale_order_ids = fields.One2many('sale.order', 'partner_id', string='Qutetions')
    invoice_ids = fields.One2many('account.move','partner_id', string='Invoices')
    invoice_line_ids = fields.One2many('account.move.line','partner_id', string='Invoices Items')
    
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel', 'blocked'):
                raise UserError('You cannot delete a student that is not in draft, cancel, or blocked state.')
        return super(StudentStudent, self).unlink()
    

    know_us = fields.Many2one('know.us', required=True, copy=True,  tracking=True,)
    partner_id = fields.Many2one('res.partner', required=True, copy=True,  tracking=True,)
    mobile = fields.Char('Mobile', required=True, copy=True, tracking=True,)
    mobile2 = fields.Char('Mobile2', required=True, copy=True,  tracking=True,)
    job_position = fields.Char('Job Position',  required=True, copy=True, tracking=True,)
    email = fields.Char('Email',  required=True,  copy=True,  tracking=True,)
    guardian_id = fields.Many2one('student.guardian',string='Guardian', required=True)
    student_date = fields.Date(string='Student Date', default=fields.Date.today(), required=True, copy=True, tracking=True, )
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.user.company_id, required=True, copy=True, )
    date_end = fields.Date( string='Student Deadline', help='Last date for the student to be needed', copy=True,)
    date_done = fields.Date( string='Date Done',  help='Date of Completion of student Student', )      
    confirm_date = fields.Date( string='Confirmed Date',copy=False,)
    userblocked_date = fields.Date(  string='Blocked Date',  readonly=True, copy=False, )
    employee_confirm_id = fields.Many2one('hr.employee', string='Confirmed by',  readonly=True,copy=False, )
    blocked_employee_id = fields.Many2one('hr.employee', string='Blocked by',  readonly=True,copy=False, )


# seq 
    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New')  and vals.get('guardian_id'):# adding add....
            guardian = self.env['student.guardian'].browse(vals['guardian_id'])#addtional
            if guardian:
                vals['number'] = guardian.number or _('New')
            vals['number'] = self.env['ir.sequence'].next_by_code('student.student.seq') or _('New')
        res = super(StudentStudent, self).create(vals)
        return res


# class Guardian(models.Model):
#     _name = 'school.guardian'
#     _description = 'Guardian'

#     # Other fields...

#     @api.model
#     def create(self, vals):
#         if vals.get('sequence', _('New')) == _('New'):
#             vals['sequence'] = self.env['ir.sequence'].next_by_code('school.guardian.seq') or _('New')
#         guardian = super(Guardian, self).create(vals)
#         return guardian

# class Student(models.Model):
#     _name = 'school.student'
#     _description = 'Student'

#     guardian_id = fields.Many2one('school.guardian', string='Guardian')
#     # Other fields...

#     @api.model
#     def create(self, vals):
#         if vals.get('number', _('New')) == _('New') and vals.get('guardian_id'):
#             guardian = self.env['school.guardian'].browse(vals['guardian_id'])
#             if guardian:
#                 vals['number'] = guardian.sequence or _('New')
#         student = super(Student, self).create(vals)
#         return student

# class Student(models.Model):
#     _name = 'school.student'
#     _description = 'Student'

    # guardian_id = fields.Many2one('school.guardian', string='Guardian')
    # Other fields...

    # @api.model
    # def create(self, vals):
    #     if vals.get('number', _('New')) == _('New') and vals.get('guardian_id'):
    #         guardian = self.env['school.guardian'].browse(vals['guardian_id'])
    #         if guardian:
    #             vals['number'] = guardian.sequence or _('New')
    #     student = super(Student, self).create(vals)
    #     return student


    def student_confirm(self):
        for rec in self:
            # manager_mail_template = self.env.ref('reg.email_confirm_school_reg_base')
            rec.employee_confirm_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.confirm_date = fields.Date.today()
            rec.state = 'active'


    @api.depends('name', 'number','family_number')
    def student_name2(self):
        for rec in self:
            rec.name2 = ''
            rec.number2 = ''
            number = rec.number
            family_number = rec.family_number
            name = rec.name or ''
            number = rec.number or ''
            name2 = rec.family_name or ''
            if family_number:
                rec.number2 = family_number + '' + number
            # rec.name = name + ' ' + name2
            # if isinstance(name, str) and isinstance(name2, str):
            #     rec.name = name + ' ' + name2
            # else:
            #     rec.name = ''

    def student_blocked(self):
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
