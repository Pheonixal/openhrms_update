from odoo import models, fields, api
import json, requests
import pymorphy2
from . import humanizator

import base64
import io, os

class HrDocumentInherit(models.Model):
    _inherit = 'hr.document'

    document_type = fields.Selection([
        ('hr_recruitment', 'О приеме на работу.'),
        ('hr_business_trip', 'О командировании'),
        ('on_taking_office', 'О вступлении в должность'),
        ('going_to_work', 'О выходе на работу'),
        ('termination_employment_contract', 'О прекращение ТД'),
        ('leave_without_pay', 'О предоставлении отпуска без сохранения заработной платы'),
        ('paid_leave', 'О предоставлении оплачиваемого трудового отпуска'),
    ])

    document_type2 = fields.Selection([
        ('hr_recruitment', 'Recruitment document2'),
        ('hr_wage', 'Wage document2'),
    ])

    employee_id = fields.Many2one('hr.employee', string='Сотрудник')
    name_boss = fields.Many2one('hr.employee', string='Руководитель')
    date_document = fields.Date(string='Дата документа')
    city_document = fields.Char(string="Город")

    number_document = fields.Char(string='Номер документа')
    employee_spec = fields.Char(string='Должность сотрудника')
    date_departure = fields.Date(string='Дата отправления')
    number_days = fields.Char(string='Срок командировки(кол. дней)')
    city_departure = fields.Char(string='Город отправления')
    date_vstupleniya_spec = fields.Date(string='Дата вступления в должность')
    future_job_spec = fields.Many2one('hr.job', string='Приступает к должности')
    number_protocol = fields.Char(string='На основании протокола')
    date_meeting = fields.Date(string='Дата собрания')
    osnovaniye = fields.Char(string='Основание')
    date_last_time_at_job = fields.Date(string='Дата последнего раб. дня')
    date_first_day_otpusk = fields.Date(string='Дата начала отпуска')
    date_last_day_otpusk = fields.Date(string='Дата окончания  отпуска')
    date_start_period = fields.Date(string='Дата начала периода')
    date_finish_period = fields.Date(string='Дата окончания периода')

    # Generation of word
    future_job_spec_gen = fields.Char()
    employee_id_gen = fields.Char(compute='_get_employee_id_name')
    date_vstupleniya_spec_gen_rus = fields.Char(compute='_get_date_vstupleniya_spec_gen_rus')
    number_document_gen = fields.Char(compute='_get_number_document_gen')
    datetime_dogovor = fields.Char(compute='_get_datetime_dogovor')
    date_vstupleniya_spec_gen_kaz = fields.Char(compute='_get_date_vstupleniya_spec_gen_kaz')
    date_employee_termination = fields.Char(compute='_get_date_termination')
    date_employee_termination_rus = fields.Char(compute='_get_date_termination_rus')
    date_first_day_otpusk_kaz = fields.Char(compute='_get_date_first_day_otpusk_kaz')
    date_last_day_otpusk_kaz = fields.Char(compute='_get_date_last_day_otpusk_kaz')
    date_first_day_otpusk_rus = fields.Char(compute='_get_date_first_day_otpusk_rus')
    date_last_day_otpusk_rus = fields.Char(compute='_get_date_last_day_otpusk_rus')
    days_difference = fields.Char(compute="_days_difference")
    employee_spec_gen = fields.Char(compute="_get_employee_spec_gen")
    employee_id_gen_dat = fields.Char(compute="_get_employee_id_gen_dat")
    employee_spec_gen_dat = fields.Char(compute="_get_employee_spec_gen_dat")
    director_spec = fields.Char(compute='_get_director_spec')
    director_spec_kaz = fields.Char(compute='_get_director_spec_kaz')
    company_id = fields.Many2one('res.partner', compute="_get_company")

    @api.onchange('name_boss')
    def _get_director_spec_kaz(self):

        print(self.name_boss.job_id.name)
        if self.name_boss.job_id.name == "Генеральный директор":
            self.director_spec_kaz = "Бас директоры"
        elif self.name_boss.job_id.name == "Заместитель директора":
            self.director_spec_kaz = "Бас директорыдың орынбасары"
        else:
            self.director_spec_kaz = "Генеральный директор"

    @api.onchange('name_boss')
    def _get_director_spec(self):
        self.director_spec = self.name_boss.job_id.name

    @api.onchange("employee_id")
    def _get_company(self):
        self.company_id = self.employee_id.address_id

    def _get_employee_spec_gen_dat(self):
        self.employee_spec_gen_dat = self.sklon_word_padezh(self.employee_spec, 'datv')

    @api.depends('employee_spec')
    def _get_employee_spec_gen(self):
        self.employee_spec_gen = self.sklon_word_padezh(str(self.employee_spec), 'gent')

    @api.depends('date_first_day_otpusk', "date_last_day_otpusk")
    def _days_difference(self):
        for rec in self:
            rec.days_difference = ""
            if rec.date_last_day_otpusk and rec.date_first_day_otpusk:
                d_lft = rec.date_last_day_otpusk - rec.date_first_day_otpusk
                rec.days_difference = max(0, d_lft.days)

    def _get_date_first_day_otpusk_kaz(self):
        for rec in self:
            rec.date_first_day_otpusk_kaz = ""
            if rec.date_first_day_otpusk != False:
                my_date = str(rec.date_first_day_otpusk).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_kaz_sklon(int(month))
                rec.date_first_day_otpusk_kaz = year + " жылдың " + " " + day + " " + month_str

    def _get_date_last_day_otpusk_kaz(self):
        for rec in self:
            rec.date_last_day_otpusk_kaz = ""
            if rec.date_last_day_otpusk != False:
                my_date = str(rec.date_last_day_otpusk).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_kaz_sklon(int(month))
                rec.date_last_day_otpusk_kaz = year + " жылдың " + " " + day + " " + month_str[:-1]

    def _get_date_first_day_otpusk_rus(self):
        for rec in self:
            rec.date_first_day_otpusk_rus = ""
            if rec.date_first_day_otpusk != False:
                my_date = str(rec.date_first_day_otpusk).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_rus(int(month))
                rec.date_first_day_otpusk_rus = day + " " + month_str + " "

    def _get_date_last_day_otpusk_rus(self):
        for rec in self:
            rec.date_last_day_otpusk_rus = ""
            if rec.date_last_day_otpusk != False:
                my_date = str(rec.date_last_day_otpusk).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_rus(int(month))
                rec.date_last_day_otpusk_rus = day + " " + month_str + " " + year

    def _get_date_termination(self):
        for rec in self:
            rec.date_employee_termination = ""
            if rec.date_last_time_at_job != False:
                my_date = str(rec.date_last_time_at_job).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_kaz(int(month))
                rec.date_employee_termination = year + " жылдың " + day + " " + month_str

    def _get_date_termination_rus(self):
        for rec in self:
            rec.date_employee_termination_rus = ""
            if rec.date_last_time_at_job != False:
                my_date = str(rec.date_last_time_at_job).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_rus(int(month))
                rec.date_employee_termination_rus = day + " " + month_str + " " + year

    number_days_rus = fields.Char(compute='_get_number_days_rus')
    number_days_kaz = fields.Char(compute='_get_number_days_kaz')

    def _get_date_vstupleniya_spec_gen_kaz(self):
        for rec in self:
            rec.date_vstupleniya_spec_gen_kaz = ""
            if rec.date_vstupleniya_spec != False:
                my_date = str(rec.date_vstupleniya_spec).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_kaz_sklon(int(month))
                rec.date_vstupleniya_spec_gen_kaz = year + " жылдың " + " " + day + " " + month_str

    def _get_datetime_dogovor(self):
        print(self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)]))
        self.datetime_dogovor = \
        str(self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)]).date_start).split(" ")[0]

    def _get_number_document_gen(self):
        self.number_document_gen = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)]).name

    @api.depends('date_vstupleniya_spec')
    def _get_date_vstupleniya_spec_gen_rus(self):
        for rec in self:
            rec.date_vstupleniya_spec_gen_rus = ""
            if rec.date_vstupleniya_spec != False:
                my_date = str(rec.date_vstupleniya_spec).split(" ")[0]
                month = my_date.split("-")[1]
                year = my_date.split("-")[0]
                day = my_date.split("-")[2]
                month_str = rec.get_month_rus(int(month))
                rec.date_vstupleniya_spec_gen_rus = day + " " + month_str + " " + year

    def get_month_rus(self, number):
        month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                 'ноября', 'декабря']
        return month[number - 1]

    def get_month_kaz(self, number):
        month = ['қаңтар', 'ақпан', 'наурыз', 'сәуір', 'мамыр', 'маусым', 'шілде', 'тамыз', 'қыркүйек', 'қазан',
                 'қараша', 'желтоқсан']
        return month[number - 1]

    def get_month_kaz_sklon(self, number):
        month = ['қаңтарынан', 'ақпанынан', 'наурызынан', 'сәуірінен', 'мамырынан', 'маусымынан', 'шілдесінен',
                 'тамызынан', 'қыркүйегінен', 'қазанынан',
                 'қарашасынан', 'желтоқсанынан']
        return month[number - 1]

    @api.depends('employee_id')
    def _get_employee_id_name(self):
        self.employee_id_gen = self.sklon_word_padezh(str(self.employee_id.name), 'gent')

    def capitalize_word(self, word1, word2):
        word2 = list(word2)
        for i in range(len(word1)):
            if str(word1[i]).isupper():
                word2[i] = word2[i].upper()
        return word2

    def listToString(self, s):
        str1 = ""
        return str1.join(s)

    def sklon_word_padezh(self, my_str, padezh):
        result_str = ""
        try:
            for i in my_str.split(" "):
                morph = pymorphy2.MorphAnalyzer()
                word = morph.parse(i)[0]

                sklon_word = word.inflect({padezh}).word
                if i.endswith('ов') or i.endswith('ев'):
                    result_str += word.inflect({'gent'}).word.capitalize() + "а" + " "
                elif i.endswith('ұлы') or i.endswith('қызы') or i.endswith('кызы') or i.endswith('улы'):
                    result_str += i + " "
                else:
                    result_str += self.listToString(self.capitalize_word(i, sklon_word)) + " "
        except:
            print("")
            return my_str
        return result_str[:-1]

    def _get_employee_id_gen_dat(self):
        self.employee_id_gen_dat = self.sklon_word_padezh(self.employee_id.name, 'datv')

    def get_padezh(self, my_str):
        result_str = ""
        try:
            if my_str != False:
                for i in my_str.split(" "):

                    morph = pymorphy2.MorphAnalyzer()
                    word = morph.parse(i)[0]
                    if i.endswith('ов') or i.endswith('ев'):
                        result_str += word.inflect({'gent'}).word.capitalize() + "а" + " "
                    else:
                        result_str += word.inflect({'gent'}).word.capitalize() + " "
        except:
            print("")
        return result_str

    @api.onchange('future_job_spec')
    def _get_future_job_gen(self):
        self.future_job_spec_gen = self.sklon_word_padezh(self.future_job_spec.name, 'gent')

    @api.onchange('employee_id')
    def _get_job_id(self):
        if self.employee_id:
            self.employee_spec = self.employee_id.job_id.name

    @api.depends('number_days')
    def _get_number_days_rus(self):
        self.number_days_rus = humanizator.num2text(int(self.number_days))

    @ api.depends('number_days')
    def _get_number_days_kaz(self):
        self.number_days_kaz = humanizator.num2words(int(self.number_days))

