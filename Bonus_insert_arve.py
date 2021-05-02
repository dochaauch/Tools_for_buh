#"06.04.20","27.04.20","1"
#"Subconto", "6:107:3","2021"
#"Subconto", "6:107:3:2",,"210226 150221","16:1","20:30","21:10.03.21","25:150221","26:26.02.21","30:26.02.21","100:25.00"
#"1","26.02.21","62","1","46","02","25.00","Mediabrands Digital OU: teenus:1 tolkimine","6:107:3:2","2:4","","",""
#"1","26.02.21","62","1","68","1","5.00","Mediabrands Digital OU: ARVE 21035  kaibemaks","6:107:3:2","12:1","","",""



import pandas as pd
from dbfread import DBF

import os
import re


list_db = [_ for _ in os.listdir(r'/Volumes/[C] Windows 10/Dropbox/_N/Bonus_2011/')
     if (_.endswith('.dbf')) or (_.endswith('.DBF'))]
for l in list_db:
    #print()
    #print('*** new ***')
    #print(l)

    path_ = f'/Volumes/*Windows 10/Dropbox/_N/Bonus_2011/{l}'



    table = DBF(path_, encoding='cp866')


    #exception_list = ['1SBSVPR.DBF', '1SBGLKN.DBF']
    sec_subkonto = []
    #
    for record in table:
        if l.lower() == '1sbspsk.dbf'.lower(): # подключаемся к таблицу субконто
            if record['SCHSKKOD'] == '    6': # выбираем субконто 6 юр.лица
                try:
                    if 'SELVER AS'.lower() in record['SPSKIM'].lower(): # ищем наименование фирмы
                        nomer_subkonto = record['SPSKNO'].strip() #определяем номер субконто
                        pattern_ = rf'^\s+{nomer_subkonto}\s+.+'
                    if re.match(pattern_, record['SPSKUP']):
                        sk = record['SPSKUP'].split()
                        #print(sk[1])
                        sec_subkonto.append(int(sk[1]))
                        print(record['SPSKUP'])

                except:
                    pass
                #print(max(sec_subkonto))

