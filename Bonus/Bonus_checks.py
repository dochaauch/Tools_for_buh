from datetime import datetime
from Bonus_scan_pdfplumber import read_db, my_reverse_date
from simpledbf import Dbf5
import pandas as pd
import numpy as np
import math

file_ = '/Users/docha/Google Диск/Bonus/_cheki/combine.csv'
dbf = Dbf5(r'/Volumes/[C] Windows 10 (1)/Dropbox/_N/Bonus_2011/1sbspsk.dbf', codec='cp866')
subkonto_yes = 1
year_arve = '2022'

today = datetime.now()
stamp = today.strftime('%m%d')

text_provodki = ''
date_list = []


def umlaut_to_string (str_):
    special_char_map = {ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
                   ord('ž'): 'z', ord('š'): 's',
                   ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
                   ord('Z'): 'Z', ord('Š'): 's', ord('’'): ''}
    return str_.translate(special_char_map)


def fl_round(str_):
    return round(float(str_), 2)


def find_subkonto_in_db(
        df_sub, nimi_df,
              uus_nr_comb,
        uus_kokku, uus_maksedate, uus_arve, uus_date, uus_kta, uus_km, nimi_arve,
        text_provodki, subkonto_yes, year_arve, ):
    """
    :param df_sub: результат read_db(dbf)
    :param nimi_df: результат read_db(dbf)
    :param uus_nr_comb: обратная дата + номер счета
    :param uus_kokku: общая сумма счета
    :param uus_maksedate: дата оплаты
    :param uus_arve: номер счета
    :param uus_date: дата счета
    :param uus_kta: сумма без налога
    :param uus_km: сумма налога
    :param nimi_arve: наименование фирмы
    :param text_provodki:
    :param subkonto_yes: создаем новый субконто или нет
    :param year_arve: год проводок
    :return:
    """
    #nomer_subkonto = int(hank_subk.split(':')[1])  #берем из csv файла
    nimi_arve_low = nimi_arve.lower()
    text_provodki_subk = ''

    if uus_kta + uus_km != uus_kokku:
        print('***', uus_kta + uus_km != uus_kokku, uus_kta + uus_km, uus_kokku, nimi_arve)

    nimi_my = nimi_df[nimi_df['SPSKIM'].str.lower().str.contains(nimi_arve_low)]  # находим строку с фирмой
    # если такой фирмы еще не существует
    if nimi_my.empty:
        nimi_firma = nimi_df['SPSKNO'].max()
        # создаем строку
        if subkonto_yes == 1:
            text_provodki_subk = f'"Subconto", "6:{nimi_firma + 1}","{nimi_arve.strip()}",,"15:1", "91:0"'
        nf_df = pd.DataFrame([[nimi_firma + 1, '6', np.nan, nimi_arve.strip(), 1]],
                             columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA'],
                             index=[len(nimi_df) + 1])

        # добавляем запись в базу с именами
        nimi_df = nimi_df.append(nf_df, ignore_index=True)

        nimi_my = nimi_df[nimi_df['SPSKIM'].str.lower().str.contains(nimi_arve_low)]  # находим строку с фирмой
        if subkonto_yes == 1:
           text_provodki += text_provodki_subk + '\r\n'

    #print(nimi_arve, nimi_my['SPSKNO'], nimi_my['SPSKNO'].max())
    nomer_subkonto = nimi_my['SPSKNO'].max()  # определяем из строки номер субконто
    #print('proverka', year_arve, nomer_subkonto,
    #          df_sub[(df_sub['SPSKIM'] == year_arve) & (df_sub['year'] == nomer_subkonto)]['SPSKNO'])

    mnr = df_sub[(df_sub['SPSKIM'] == year_arve) & (df_sub['year'] == nomer_subkonto)]['SPSKNO'].max()
    #print('mnr', mnr)
    #if math.isnan(mnr):
    #    print('mnr is nan')
    #try:
    max_nre_year = df_sub[(df_sub['SPSKIM'] == year_arve) & (df_sub['year'] == nomer_subkonto)]['SPSKNO'].max()
    #print('max_nre_year', max_nre_year)

    if math.isnan(max_nre_year):
    #except:  # в случае, если фирма старая, но этот год был еще не введен
        #print('year_arve', year_arve, df_sub[(df_sub['SPSKIM'] == year_arve) & (df_sub['year'] == nomer_subkonto)]['SPSKNO'])
        #print('xxx', df_sub[(df_sub['arve'] == 0)]['SPSKNO'])
        #print('check_', df_sub['year'], nomer_subkonto, nimi_arve)
        last_used_year = df_sub[(df_sub['year'] == nomer_subkonto) & (df_sub['arve'] == 0)]['SPSKNO'].max()

        if math.isnan(last_used_year):
            last_used_year = 0
        #print('last_used_year', nimi_arve, last_used_year)

        if subkonto_yes == 1:
            #if last_used_year == 0:
            #    text_provodki_subk = f'"Subconto", "6:{nomer_subkonto}","{nimi_arve.strip()}",,"15:1", "91:0"\r\n'
            text_provodki_year = f'"Subconto", "6:{nomer_subkonto}:{last_used_year + 1}","{year_arve}",,'
        year_df = pd.DataFrame([[last_used_year + 1, '6', int(nomer_subkonto), year_arve, 0.0, int(nomer_subkonto), 0]],
                               columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                        'year', 'arve'],
                               index=[len(df_sub) + 1])
        max_nre_year = last_used_year + 1
        df_sub = df_sub.append(year_df, ignore_index=True)
        if subkonto_yes == 1:
            #text_provodki += text_provodki_subk + text_provodki_year + '\r\n' тут проверить, что с годом!
            text_provodki += text_provodki_year + '\r\n'

    #ищем номер последнего счета в базе
    last_nr = df_sub[(df_sub['year'] == nomer_subkonto) & (df_sub['arve'] == max_nre_year)]['SPSKNO'].max()
    if np.isnan(last_nr):
        arve_df = pd.DataFrame([[1, '6', int(nomer_subkonto), year_arve, 0.0, int(nomer_subkonto), 1]],
                               columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                                        'year', 'arve'],
                               index=[len(df_sub) + 1])
        df_sub = df_sub.append(arve_df, ignore_index=True)
        last_nr = 1
    else:
        arve_df = pd.DataFrame(
            [[last_nr + 1, '6', int(nomer_subkonto), last_nr, 0.0, int(nomer_subkonto), max_nre_year]],
            columns=['SPSKNO', 'SCHSKKOD', 'SPSKUP', 'SPSKIM', 'SPSKCENA',
                     'year', 'arve'],
            index=[len(df_sub) + 1])
        df_sub = df_sub.append(arve_df, ignore_index=True)
        last_nr = last_nr + 1

    if subkonto_yes == 1:
        subkonto_jur = f'6:{nomer_subkonto}:{max_nre_year}:{last_nr}'
        text_provodki_arve = (f'"Subconto", "6:{nomer_subkonto}:{max_nre_year}:{last_nr}","{uus_nr_comb}",,"15:1",'
                              f'"20:{uus_kokku}","21:{uus_maksedate}","25:{uus_arve}","26:{uus_date}",'
                              f'"30:{uus_date}"')
    else:
        text_provodki_arve = ''

    text_provodki += text_provodki_arve
    return nimi_df, df_sub, text_provodki, subkonto_jur

df_sub, nimi_df = read_db(dbf)


with open(file_, 'r') as csv_file:
    lines = csv_file.readlines()[1:]

    for l in lines:
        text_provodki_km = ''
        text_provodki_auto = ''
        subkonto_kulud = ''
        linie = l.split(',')

        n, kuupaev, firma, regnr, arve_nr, summa_ilma, km, summa, kirjeldus, auto, not_changed, *oth = \
            [s.strip() for s in linie]

        uus_nr_comb = my_reverse_date(kuupaev) + ' ' + arve_nr
        nr = kuupaev.split('.')[2] + kuupaev.split('.')[1]
        firma = umlaut_to_string(firma)
        firma_ = firma[:7].strip()
        kirjeldus = umlaut_to_string(kirjeldus)
        kirjeldus_ = kirjeldus.split(' ')[-1]
        arve_nr = arve_nr[-10:].strip()

        dict_for_subkonto = {'bensiin': '8:6:25:2',
                             'arvuti': '8:6:11:24',
                             'pesula': '8:6:25:6',
                             'auto': '8:6:25:7',
                             'puhastusvahend': '8:6:28:1',
                             'ruum': '8:6:1:10'}
        for k in dict_for_subkonto.keys():
            if k in kirjeldus:
                subkonto_kulud = dict_for_subkonto.get(k)
                break


        if auto == '1':
            km_ = round(float(km) / 2, 2)
            summa_ilma_ = round(float(summa) - km_, 2)
            summa_ = fl_round(summa)
        else:
            km_ = fl_round(km)
            summa_ilma_ = fl_round(summa_ilma)
            summa_ = fl_round(summa)

        nimi_df, df_sub, text_provodki_new_sub, subkonto_jur = find_subkonto_in_db(df_sub, nimi_df, uus_nr_comb, summa_, '',
                                                                           arve_nr,kuupaev, summa_ilma_, km_,
                                                                           firma, '', subkonto_yes, year_arve)

        if text_provodki_new_sub:
            text_provodki_new_sub = text_provodki_new_sub + '\r\n'
        text_provodki_1 = (
            f'"AV", "{kuupaev}","26","","60","12",{summa_ilma_},"{stamp} {firma_} {arve_nr} {kirjeldus_} {summa_ilma}/{km}", '
            f'"{subkonto_kulud}","{subkonto_jur}",""')
        text_provodki_km = (
            f'"AV", "{kuupaev}","68","1","60","12",{km_},"{stamp} {firma_} {arve_nr} {kirjeldus_} KM {summa_ilma}/{km}", '
            f'"15:11","{subkonto_jur}",""')
        text_provodki_kinni = (
            f'"AV", "{kuupaev}","60","12","71","03",{summa_},"{stamp} {firma_} {arve_nr} {kirjeldus_} {summa}", '
            f'"{subkonto_jur}","4:1",""')
        if auto == '1':
            text_provodki_auto = (
            f'"AV", "{kuupaev}","SO","K1","SO","1",{km_},"{stamp} KM {firma_} {arve_nr} {kirjeldus_} {summa_ilma}/{km}", '
            f'"24:2","24:2",""'
            '\r\n'
            f'"AV", "{kuupaev}","SO","KU","SO","1",{summa_ilma_},"{stamp} {firma_} {arve_nr} {kirjeldus_} {summa_ilma}/{km}", '
            f'"24:2","24:2",""'
            f'\r\n')
        text_provodki += text_provodki_new_sub + text_provodki_1 + '\r\n' + text_provodki_km + '\r\n' \
                         + text_provodki_kinni + '\r\n' + text_provodki_auto
        date_ = datetime.strptime(kuupaev, '%d.%m.%y')
        date_list.append(date_)

    min_date = min(date_list)
    min_date = datetime.strftime(min_date, '%d.%m.%y')
    max_date = max(date_list)
    max_date = datetime.strftime(max_date, '%d.%m.%y')

    first_row = f'"{min_date}", "{max_date}","AV"' + '\r\n'

    out = first_row + text_provodki
    print()
    print(out)
    v = open('/Volumes/[C] Windows 10 (1)/Dropbox/_N/Bonus_2011/avanss.txt', 'w')
    v.write(out)
    v.close()