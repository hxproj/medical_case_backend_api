# -*- coding:utf-8 -*-
import os
import sys
from docx import Document
from src import app
from src.entity.illness_history import Illness_history
from src.entity.oral_examination import Oral_examination
from src.entity.personal_history import Personal_history
from src.entity.tooth_location import Tooth_location
from src.entity.user import User


def generate_docx(tooth_id):
    path = os.path.abspath('./templete/illness.docx')
    document = Document(path)
    paragraphs = document.paragraphs
    full_text = ''
    for graphs in paragraphs:
        full_text = full_text + '%split%' + graphs.text
    dit = _get_dictionary(tooth_id)
    for key, value in dit.items():
       full_text = full_text.replace(key, str(dit[key]))
    text_list = full_text.split('%split%')
    text_list.remove('')
    for i in range(len(text_list)):
        if len(paragraphs[i].runs)>1:
            if not paragraphs[i].runs[0].font.bold:
                paragraphs[i].text = text_list[i]
    document.save('D:/test.docx') #todo add function to generate doc path to save


def _get_dictionary(tooth_id):
    reload(sys)
    sys.setdefaultencoding('utf8')
    tooth_location = Tooth_location.query.filter_by(tooth_id=tooth_id).first()
    user_id = tooth_location.user_id
    user = User.query.filter_by(user_id=user_id).first()
    illness_history = Illness_history.query.filter_by(tooth_id=tooth_id).first()
    personal_history = Personal_history.query.filter_by(user_id=user_id).first()
    oral_examination = Oral_examination.query.filter_by(tooth_id=tooth_id).first()
    full_dict = dict(tooth_location.get_dict().items() + user.get_dict().items() + illness_history.get_dict().items()
                     + personal_history.get_dict().items() + oral_examination.get_dict().items())
    for key, value in full_dict.items():
        if value == '是':
            full_dict[key] = '有'
        elif value == '否':
            full_dict[key] = '无'
    if full_dict['is_fill_tooth'] == 0:
        full_dict['tooth_info'] = full_dict['tooth_location'] + full_dict['symptom'] + full_dict['time_of_occurrence']
    else:
        full_dict['tooth_info'] = full_dict['tooth_location'] + '要求补牙'
    if full_dict['is_primary'] == 1:
        full_dict[
            'illness_history'] = '原发性龋病：{0}{1}前发现牙齿{2}，' \
                                 '近来症状{3}加重，{4}自发痛，夜间痛，' \
                                 '{5}服用药物（{6}），{7}做过治疗，' \
                                 '症状{8}缓解。'.format(full_dict['tooth_location'], full_dict['time_of_occurrence'],
                                                   full_dict['symptom'], full_dict['is_very_bad'],
                                                   full_dict['is_night_pain_self_pain'],
                                                   full_dict['is_medicine'], full_dict['medicine_name'],
                                                   full_dict['treatment'], full_dict['is_relief'])
    else:
        full_dict['illness_history'] = '有治疗史的龋病：{0}{1}曾行修复治疗（{2}）' \
                                       '，{3}{4}，{5}服用药物（{6}），' \
                                       '症状{7}缓解。'.format(full_dict['tooth_location'],
                                                         full_dict['time_of_occurrence'],
                                                         full_dict['fill_type'],
                                                         full_dict['time_of_occurrence'],
                                                         full_dict['symptom'],
                                                         full_dict['is_medicine'],
                                                         full_dict['medicine_name'],
                                                         full_dict['is_relief'])
    if full_dict['gender'] == True:
        full_dict['gender'] = '女'
    else:
        full_dict['gender'] = '男'
    level_list = ['-', '+-', '+', '++', '+++']
    full_dict['hot'] = level_list[full_dict['hot'] - 1]
    full_dict['cold'] = level_list[full_dict['cold'] - 1]
    full_dict['touch'] = level_list[full_dict['touch'] - 1]
    full_dict['bite'] = level_list[full_dict['bite'] - 1]
    new_dict = {}
    for key, value in full_dict.items():
        new_dict['{[' + key + ']}'] = full_dict[key]
    return new_dict
