# -*- coding:utf-8 -*-
from src import db

class Difficulty_assessment(db.Model):
    tooth_id  = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    tooth_surface_and_location = db.Column(db.String(20))
    caries_depth = db.Column(db.String(20))
    technology_type = db.Column(db.String(20))
    history_of_fill = db.Column(db.String(20))
    mouth_opening = db.Column(db.String(20))
    gag_reflex = db.Column(db.String(20))
    saliva = db.Column(db.String(20))
    dental_phobia = db.Column(db.String(20))
    difficulty_rating = db.Column(db.String(20))
    difficulty_level = db.Column(db.Integer)

    def get_dict(self):
        dit = self.__dict__
        del dit['_sa_instance_state']
        return dit
    def _caculate_difficulty(self):
        level1 =0
        level2 =0
        level3 =0
        for name, value in vars(self).items():
            if name!= '_sa_instance_state':
                value = value.encode('utf-8')
            if value in set_A:
                level1=level1+1
            elif value in set_B:
                level2 = level2+1
            elif value in set_C:
                level3=level3+1
        if level3!=0:
            return 3
        elif level3==0 and level2==0:
            return 1
        elif level2!=0 and level3==0:
            return 2


set_A = set(['Ⅴ类洞','Ⅰ类洞','浅龋','中龋','后牙复合树脂修复','后牙银汞合金修复'
                ,'ART修复','预防性填充','玻璃离子过渡性修复','釉质成型术','微创磨术'
             ,'患牙有充填修复史，但龋坏未累及旧修复体','3指宽','无','正常','低、中危人群'])

set_B = set(['Ⅱ类洞','Ⅲ类洞','Ⅳ类洞','Ⅵ类洞','根面龋(累及唇颊面)','深龋','前牙复合树脂修复','龋坏累及旧修复体或旧修复体首次折裂','2指宽','有','较多','高危人群'])

set_C = set(['后牙远中邻面龈方1/3洞','磨耗牙','牙尖缺损','严重缺损的残冠','猛性龋','根面龋(累及2个面以上)','年轻恒牙深龋','前牙无创美容修复'
                ,'前牙微创复合树脂分层修复','前牙微创CAD/CAM瓷贴面修复','后牙复合树脂嵌体'
                ,'后牙CAD/CAM瓷嵌体修复','患牙的旧修复体脱落2次或2次以上','2指宽以下','强烈','非常多','极高危人群'])
