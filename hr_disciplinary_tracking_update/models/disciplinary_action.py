# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class InheritEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_discipline_count(self):
        all_actions = self.env['disciplinary.action'].read_group([
            ('employee_name', 'in', self.ids),
            ('state', '=', 'explain'),
        ], fields=['employee_name'], groupby=['employee_name'])
        mapping = dict([(action['employee_name'][0], action['employee_name_count']) for action in all_actions])
        for employee in self:
            employee.discipline_count = mapping.get(employee.id, 0)

    disciplinary_line_ids = fields.One2many('disciplinary.action', 'employee_name', string="Disciplinary actions")

    just_field = fields.Char(string='Just Field')
    display_type = fields.Selection([('classic', 'Classic')], string="Display Type", default='classic')


class CategoryDiscipline(models.Model):
    _inherit = 'discipline.category'
    _description = 'Reason Category'

    # Discipline Categories

    name = fields.Char(string="Name", required=True, help="Category name", translate=True)


class DisciplinaryAction(models.Model):
    _inherit = 'disciplinary.action'


    def _get_default_content(self):
        result = """<div class=\"oe_form_field oe_form_field_html o_field_widget\" name=\"content\" data-original-title=\"\" title=\"\"><div class=\"o_readonly\"><p class=\"MsoNormal\"><font style=\"font-size: 18px;\"><b>Дисциплинарные взыскания</b></font></p><p class=\"MsoNormal\"><font style=\"font-size: 18px;\"><b><br></b></font></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">РК от 24.05.18 г. № 156-VI
                    (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=36861709#sub_id=640100\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1. За совершение работником дисциплинарного проступка работодатель или
                    первый руководитель национального управляющего холдинга в случаях, предусмотренных
                    законами Республики Казахстан, вправе применить следующие виды дисциплинарных
                    взысканий:</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1) замечание;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2) выговор;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">3) строгий выговор;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:#212529;mso-fareast-language:
                    RU\"><br>
                    <!--[if !supportLineBreakNewLine]--><br>
                    <!--[endif]--></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">В подпункт 4 внесены
                    изменения в соответствии с&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=34010504#sub_id=64\"><span style=\"color:navy\">Законом</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 04.05.20 г. № 321-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=35273177#sub_id=640000\" title=\"(СТАРАЯ РЕДАКЦИЯ) ТРУДОВОЙ КОДЕКС РЕСПУБЛИКИ КАЗАХСТАН ОТ 23 НОЯБРЯ 201...\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">4) расторжение трудового договора по инициативе работодателя по основаниям,
                    предусмотренным&nbsp;</span><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:#333399;mso-fareast-language:
                    RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=38910832#sub_id=520108\" title=\"Трудовой кодекс Республики Казахстан от 23 ноября 2015 года № 414-V (с изменениями и дополнениями по состоянию на 13.05.2020 г.)\"><span style=\"color:#333399\">подпунктами 8), 9), 10), 11), 12), 14), 15), 16), 17) и
                    18) пункта 1 статьи 52</span></a></span></u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:black;mso-fareast-language:RU\">&nbsp;настоящего Кодекса.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2. Применение дисциплинарных взысканий, не предусмотренных настоящим
                    Кодексом и иными законами Республики Казахстан, не допускается.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">См.:&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=35071444#sub_id=3000\" title=\"Нормативное постановление Верховного Суда Республики Казахстан от 6 октября 2017 года № 9 \"><span style=\"color:navy\">Нормативное постановление</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">&nbsp;Верховного Суда Республики
                    Казахстан от 6 октября 2017 года № 9 «О некоторых вопросах применения судами
                    законодательства при разрешении трудовых споров»</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\"></p><p>&nbsp;</p><p></p><p class=\"MsoNormal\" style=\"margin: 0cm 0cm 0.0001pt 60pt; text-align: justify; text-indent: -40pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><b><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\">Статья 65. Порядок
                    применения дисциплинарных взысканий</span></b><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">Пункт 1 изложен в
                    редакции&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=36227306#sub_id=1265\"><span style=\"color:navy\">Закона</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 24.05.18 г. № 156-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=36861709#sub_id=650000\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">); внесены изменения в
                    соответствии с&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:
                    &quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;
                    mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=34010504#sub_id=65\"><span style=\"color:navy\">Законом</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 04.05.20 г. № 321-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=35273177#sub_id=650000\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1. Дисциплинарное взыскание налагается работодателем путем издания акта
                    работодателя, за исключением случаев, предусмотренных законами Республики
                    Казахстан. При наложении дисциплинарного взыскания первым руководителем
                    национального управляющего холдинга в случаях, предусмотренных законами Республики
                    Казахстан, применяются положения настоящей статьи и&nbsp;</span><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=38910832#sub_id=660000\"><span style=\"color:navy\">статьи 66</span></a></span></u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:black;mso-fareast-language:RU\">&nbsp;настоящего Кодекса.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2. До применения дисциплинарного взыскания работодатель обязан затребовать
                    от работника письменное объяснение. Если по истечении двух рабочих дней
                    письменное объяснение работником не представлено, то составляется
                    соответствующий акт.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">Непредоставление работником объяснения не является препятствием для
                    применения дисциплинарного взыскания.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">3. За каждый дисциплинарный проступок к работнику может быть применено
                    только одно дисциплинарное взыскание.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">4. Акт работодателя о наложении на работника дисциплинарного взыскания не
                    может быть издан в период:</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1) временной нетрудоспособности работника;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2) освобождения работника от работы на время выполнения государственных или
                    общественных обязанностей;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">3) нахождения работника в отпуске или межвахтовом отдыхе;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">4) нахождения работника в командировке;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">Пункт дополнен подпунктом
                    5 в соответствии с&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=34010504#sub_id=65\"><span style=\"color:navy\">Законом</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 04.05.20 г. № 321-VI</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">5) проведения расследования несчастного случая, связанного с трудовой
                    деятельностью, в отношении лиц, допустивших нарушения требований по
                    безопасности и охране труда.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">См.:&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=33344384\"><span style=\"color:navy\">Ответ</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;Министра труда и социальной защиты
                    населения РК от 26 августа 2019 года на вопрос от 13 августа 2019 года № 562801
                    (dialog.gov.kz) «О наложении дисциплинарного взыскания на сотрудника в период
                    отстранения его от работы»</span></i><span style=\"font-size:12.0pt;font-family:
                    &quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;
                    mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">В пункт 5 внесены
                    изменения в соответствии с&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=34010504#sub_id=65\"><span style=\"color:navy\">Законом</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 04.05.20 г. № 321-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=35273177#sub_id=650500\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">5. Акт о наложении дисциплинарного взыскания объявляется работнику,
                    подвергнутому дисциплинарному взысканию, под роспись в течение трех рабочих
                    дней со дня его издания. В случае отказа работника подтвердить своей подписью
                    ознакомление с актом работодателя об этом делается соответствующая запись в
                    акте о наложении дисциплинарного взыскания.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">В случае невозможности ознакомить работника лично с актом работодателя о
                    наложении дисциплинарного взыскания работодатель обязан направить работнику
                    копию акта о наложении дисциплинарного взыскания по почте заказным письмом
                    с&nbsp;</span><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=38910832#sub_id=10181\"><span style=\"color:navy\">уведомлением</span></a></span></u><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:black;mso-fareast-language:RU\">&nbsp;о его вручении в течение трех
                    рабочих дней со дня издания акта работодателя.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">См.:&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=35071444#sub_id=1700\"><span style=\"color:navy\">Нормативное постановление</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">&nbsp;Верховного Суда
                    Республики Казахстан от 6 октября 2017 года № 9 «О некоторых вопросах
                    применения судами законодательства при разрешении трудовых споров»</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">&nbsp;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin: 0cm 0cm 0.0001pt 60pt; text-align: justify; text-indent: -40pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><b><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\">Статья 66. Сроки
                    наложения и действия дисциплинарного взыскания</span></b><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1. Дисциплинарное взыскание на работника налагается непосредственно при
                    обнаружении дисциплинарного проступка, но не позднее одного месяца со дня его
                    обнаружения, за исключением случаев, предусмотренных&nbsp;</span><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:#333399;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=38910832#sub_id=650400\"><span style=\"color:#333399\">пунктом 4 статьи 65</span></a></span></u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\">&nbsp;настоящего Кодекса
                    и другими законами Республики Казахстан.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">В случаях, предусмотренных&nbsp;</span><u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:#333399;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=38910832#sub_id=1760000\"><span style=\"color:#333399\">статьей 176</span></a></span></u><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:black;mso-fareast-language:RU\">&nbsp;настоящего Кодекса, дисциплинарные
                    взыскания налагаются не позднее одного месяца со дня вступления в законную силу
                    решения суда о признании забастовки незаконной.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">Пункт 2 изложен в
                    редакции&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=32487946#sub_id=66\"><span style=\"color:navy\">Закона</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 26.11.19 г. № 273-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=37955445#sub_id=660200\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 21.3pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2. Дисциплинарное взыскание не может быть применено позднее шести месяцев
                    со дня совершения дисциплинарного проступка, а в случаях, установленных
                    законами Республики Казахстан, или установления дисциплинарного проступка по результатам
                    ревизии или проверки финансово-хозяйственной деятельности работодателя -
                    позднее одного года со дня совершения работником дисциплинарного проступка.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">Пункт 3 изложен в
                    редакции&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=32487946#sub_id=66\" title=\"Закон Республики Казахстан от 26 ноября 2019 года № 273-VI \"><span style=\"color:navy\">Закона</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 26.11.19 г. № 273-VI (</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=37955445#sub_id=660300\"><span style=\"color:navy\">см. стар. ред.</span></a></span></u></i><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">)</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">3.&nbsp;Рассмотрение вопроса о дисциплинарной ответственности и течение
                    срока наложения дисциплинарного взыскания приостанавливаются в период:</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">1) отсутствия работника на работе в связи с временной нетрудоспособностью;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">2) освобождения от работы для выполнения государственных или общественных
                    обязанностей;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">3) нахождения в отпуске, командировке или межвахтовом отдыхе;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">4) производства по уголовному делу, делу об административном
                    правонарушении, а также до вступления в законную силу судебного акта или акта
                    должностного лица, уполномоченного рассматривать дела об административных
                    правонарушениях, влияющего на решение вопроса о дисциплинарной ответственности
                    работника;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">5) нахождения работника на подготовке, переподготовке, курсах повышения
                    квалификации и стажировке;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">6) обжалования работником в судебном порядке актов работодателя о
                    совершении им дисциплинарного проступка;</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">Пункт дополнен подпунктом
                    7 в соответствии с&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;
                    font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=34010504#sub_id=66\"><span style=\"color:navy\">Законом</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;РК от 04.05.20 г. № 321-VI</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 19.85pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">7) проведения расследования несчастного случая, связанного с трудовой
                    деятельностью, в отношении лиц, допустивших нарушения требований по
                    безопасности и охране труда.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:red;mso-fareast-language:RU\">См.:&nbsp;</span></i><i><u><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:navy;mso-fareast-language:RU\"><a href=\"https://online.zakon.kz/Document/?doc_id=31784899\"><span style=\"color:navy\">Ответ</span></a></span></u></i><i><span style=\"font-size:
                    12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:&quot;Times New Roman&quot;;
                    color:red;mso-fareast-language:RU\">&nbsp;Министра труда и социальной защиты
                    населения РК от 22 октября 2019 года на вопрос от 10 октября 2019 года № 574574
                    (dialog.gov.kz) «О приостановлении шестимесячного срока со дня совершения
                    дисциплинарного проступка в случае временной нетрудоспособности работника»</span></i><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;mso-fareast-font-family:
                    &quot;Times New Roman&quot;;color:black;mso-fareast-language:RU\"></span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">4. Срок действия дисциплинарного взыскания не может превышать шесть месяцев
                    со дня его применения, за исключением расторжения трудового договора по
                    основаниям, предусмотренным настоящим Кодексом.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\">5. Работодатель, наложивший на работника дисциплинарное взыскание, вправе
                    снять его досрочно путем издания акта работодателя.</span></p><p></p><p></p><p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify; text-indent: 20pt; line-height: normal; background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; vertical-align: baseline;\"><span style=\"font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;
                    mso-fareast-font-family:&quot;Times New Roman&quot;;color:black;mso-fareast-language:
                    RU\"><br></span></p><p></p><p></p></div></div>"""
        return result


    date_disciplinary = fields.Date()
    date_action = fields.Date()
    description = fields.Text(string="Description")
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")
    display_type = fields.Selection([('classic', 'Classic')], string="Display Type", default='classic')
    content = fields.Html('Content', default=_get_default_content, readonly=True)

