#todo: нужно разобрать работающий код на отдельные функции, чтобы можно было
#использовать для создания файла загрузки как исходящих так и входящих счетов
#создание файла для загрузки выставленных счетов Bonus
import pandas as pd

from simpledbf import Dbf5
import re
import numpy as np

from icecream import ic
from datetime import datetime
from decimal import Decimal


def change_to_float(i):
    uus_some = line.split('\t')[i]
    uus_some = uus_some.replace(',', '.')
    uus_some = Decimal(uus_some)
    uus_some = format(uus_some, '.2f')
    uus_some = Decimal(uus_some)
    return uus_some


def time_format():
    return f'{datetime.now()}|> '


ic.configureOutput(prefix=time_format, includeContext=True)

subkonto_yes = 1  # 1 создавать новые субконто. 0 не создавать новые субконто

year_arve = '2021'
period_arve = f'"01.07.21","31.07.21","1L"' + '\r\n'


dbf = Dbf5(r'/Volumes/[C] Windows 10/Dropbox/_N/Bonus_2011/1sbspsk.dbf', codec='cp866')

def read_db(dbf):
    df = dbf.to_dataframe()

    df_jur = df[df['SCHSKKOD'] == '6'].astype({'SPSKNO':'int64'})  # выбираем только юр.лица код 6
    df_jur.SPSKNO = df_jur.SPSKNO.astype('int64')


    nimi_df = df_jur.loc[df_jur['SPSKUP'].isnull()]  # база с названиями фирм
    df_sub = df_jur.loc[df_jur['SPSKUP'].notnull()]  # база с субконто второго и третьего уровня


    #делим столбец 'SPSKUP' на 2 отдельных
    d = pd.DataFrame(df_sub['SPSKUP'].str.split().tolist(), columns=['year', 'arve'])
    df_sub = pd.concat([df_sub.reset_index(drop=True), d.reset_index(drop=True)], axis=1)
    df_sub['arve'] = df_sub['arve'].fillna(0)
    df_sub['year'] = df_sub['year'].astype('int64')
    df_sub['arve'] = df_sub['arve'].astype('int64')
    return df_sub, nimi_df

text_provodki = ''

with open('Bonus/output.txt', 'r') as f:
    lines = f.readlines()[1:-2]  # пропускаем строку с заголовками и 2 последние итоговые строки
    for line in lines:
        # собираем данные со счетов
        uus_makseaeg = int(line.split('\t')[0].strip())
        d, m, y = line.split('\t')[1].strip().split('.')
        uus_date = f'{d}.{m}.{y[2:]}'
        lausendi_date = uus_date
        uus_arve = line.split('\t')[4].strip()
        uus_nr_comb = f'{y[2:]}{m}{d} {uus_arve}'
        d, m, y = line.split('\t')[2].strip().split('.')
        uus_maksedate = f'{d}.{m}.{y[2:]}'
        uus_kokku = change_to_float(5)
        uus_km = change_to_float(6)
        uus_kta = change_to_float(7)

        if round(uus_kokku / Decimal(1.2), 2) != uus_kta or uus_kta + uus_km != uus_kokku:
            ic('не сходится налог!', uus_nr_comb, round(uus_kokku / Decimal(1.2), 2), '<>', uus_kta)
        nimi_orig = line.split('\t')[3].strip()
        nimi_orig = re.sub(r'(^.+)\bOU\b.+', r'\1', nimi_orig)  # ищем, где не стоит запятая перед адресом
        nimi_arve = nimi_orig.lower()

        nimi_arve = re.sub(r'(^\bas\b)', r'', nimi_arve).strip()
        nimi_arve = re.sub(r'(\bas\b)', r'', nimi_arve).strip()
        nimi_arve = re.sub(r'(^ou\s)', r'', nimi_arve).strip()
        nimi_arve = re.sub(r'(\s\bou\b)', r'', nimi_arve).strip()

        nimi_my = nimi_df[nimi_df['SPSKIM'].str.lower().str.contains(nimi_arve)]  # находим строку с фирмой

        # если такой фирмы еще не существует
        if nimi_my.empty:
            nimi_firma = nimi_df['SPSKNO'].max()
            # создаем строку
            if subkonto_yes == 1:
                text_provodki_subk = f'"Subconto", "6:{nimi_firma + 1}","{nimi_orig.strip()}",,"16:1", "91:0"'
                print(text_provodki_subk)
            nf_df = pd.DataFrame([[nimi_firma + 1, '6', np.nan, nimi_orig.strip(), 1]],
                              columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA'],
                                 index=[len(nimi_df) + 1])

            # добавляем запись в базу с именами
            nimi_df = nimi_df.append(nf_df, ignore_index=True)
            nimi_my = nimi_df[nimi_df['SPSKIM'].str.lower().str.contains(nimi_arve)]  # находим строку с фирмой

            if subkonto_yes == 1:
               text_provodki += text_provodki_subk + '\r\n'

        nomer_subkonto = nimi_my['SPSKNO'].item()  # определяем из строки номер субконто

        # проверяем, что у нас с годом
        if df_sub[(df_sub['year'] == nomer_subkonto)].empty:  # если это совсем новая фирма
            if subkonto_yes == 1:
                text_provodki_year = f'"Subconto", "6:{nimi_firma + 1}:1","{year_arve}",,'
            year_df = pd.DataFrame([[1, '6', int(nomer_subkonto), year_arve, 0.0, int(nomer_subkonto), 0]],
                                 columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                          'year', 'arve'],
                                 index=[len(df_sub) + 1])
            df_sub = df_sub.append(year_df, ignore_index=True)
            if subkonto_yes == 1:
                text_provodki += text_provodki_year + '\r\n'

        # находим субконто второго уровня с годом, указанным наверху
        try:
            max_nre_year = df_sub[(df_sub['SPSKIM'] == year_arve) & (df_sub['year'] == nomer_subkonto)]['SPSKNO'].item()
        except:  # в случае, если фирма старая, но этот год был еще не введен
            last_used_year = df_sub[(df_sub['year'] == nomer_subkonto) & (df_sub['arve'] == 0)]['SPSKNO'].max()

            if subkonto_yes == 1:
                text_provodki_year = f'"Subconto", "6:{nomer_subkonto}:{last_used_year + 1}","{year_arve}",,'
            year_df = pd.DataFrame([[last_used_year + 1, '6', int(nomer_subkonto), year_arve, 0.0, int(nomer_subkonto), 0]],
                                   columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                            'year', 'arve'],
                                   index=[len(df_sub) + 1])
            max_nre_year = last_used_year + 1
            df_sub = df_sub.append(year_df, ignore_index=True)
            if subkonto_yes == 1:
                text_provodki += text_provodki_year + '\r\n'

        # находим последний счет в указанном году (субконто третьего уровня)
        last_nr = df_sub[(df_sub['year'] == nomer_subkonto) & (df_sub['arve'] == max_nre_year)]['SPSKNO'].max()
        if np.isnan(last_nr):

            arve_df = pd.DataFrame([[1, '6', int(nomer_subkonto), year_arve, 0.0, int(nomer_subkonto), 1]],
                                   columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                            'year', 'arve'],
                                   index=[len(df_sub) + 1])
            df_sub = df_sub.append(arve_df, ignore_index=True)
            last_nr = 1

        else:

            arve_df = pd.DataFrame([[last_nr + 1, '6', int(nomer_subkonto), last_nr, 0.0, int(nomer_subkonto), max_nre_year]],
                                   columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                            'year', 'arve'],
                                   index=[len(df_sub) + 1])
            df_sub = df_sub.append(arve_df, ignore_index=True)
            last_nr = last_nr + 1

        text_provodki_arve = ''

        if subkonto_yes == 1:
            text_provodki_arve = (f'"Subconto", "6:{nomer_subkonto}:{max_nre_year}:{last_nr}","{uus_nr_comb}",,"16:1",'
                              f'"20:{uus_kokku}","21:{uus_maksedate}","25:{uus_arve}","26:{uus_date}",'
                              f'"30:{lausendi_date}","100:{uus_kta}"') + '\r\n'

        text_km = (f'"1L","{lausendi_date}","62","1","68","1","{uus_km}",'
                      f'"{nimi_orig.strip()}: ARVE {uus_arve}  kaibemaks",'
                   f'"6:{nomer_subkonto}:{max_nre_year}:{last_nr}","15:1","","",""')

        text_summa = (f'"1L","{lausendi_date}","62","1","46","02","{uus_kta}",'
                      f'"{nimi_orig.strip()}: teenus:1 tolkimine",'
                      f'"6:{nomer_subkonto}:{max_nre_year}:{last_nr}","2:4","","",""')
        text_provodki += text_provodki_arve + text_km + '\r\n' + text_summa + '\r\n'

out = f"""{period_arve}{text_provodki}"""

new_f = open('/Volumes/[C] Windows 10/Dropbox/_N/Bonus_2011/BA_output.txt', 'w')
new_f.write(out)
new_f.close()
