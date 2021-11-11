import pdfplumber
from collections import namedtuple, defaultdict
import re
import os
import pprint
from decimal import Decimal
import csv
import datetime
from simpledbf import Dbf5
import pandas as pd
import numpy as np




def read_csv_to_dict_template(path):
    with open(path, newline='') as inp:
        reader = csv.DictReader(inp)
        template_dict = {row.pop('firma'): row for row in reader}
    return template_dict


def find_all_files(your_target_folder, r1, in_or_out):
    pdf_files = []
    full_list = []
    for dirpath, _, filenames in os.walk(your_target_folder):
        for items in filenames:
            file_full_path = os.path.abspath(os.path.join(dirpath, items))
            if file_full_path.endswith('.pdf'):
                full_list.append(file_full_path)
            if r1.search(file_full_path.lower()): #  ищем наш паттерн в полном пути файла
                pdf_files.append(file_full_path)
            else:
                pass
    pdf_files.sort(key=str.lower)
    #pprint.pprint(pdf_files)
    if in_or_out == 1:
        file_list = list(set(full_list) - set(pdf_files))
    else:
        file_list = pdf_files
    return file_list


def read_pdf_to_text_in_folder(pdf_files):
    text_dict = {}
    for ap in pdf_files:
        with pdfplumber.open(ap) as pdf:
            page = pdf.pages[0]  # читаем только первую страницу в пдф
            text = page.extract_text()
            key = os.path.basename(ap)
            text_dict[key] = text
    return text_dict


def my_str_to_float(str_):
    # str_ '13,50' => float '13.5'
    return Decimal(str_.replace(',', '.'))


def my_short_date(str_):
    # '21.05.2021' => '21.05.21'
    return str_[:6] + str_[-2:]


def my_reverse_date(str_):
    # '21.05.2021' , '21.05.21' => 210521
    return str_[-2:] + str_[3:5] + str_[:2]


def find_in_template_dict(t_nimi, str_, template_dict):
    return template_dict.get(t_nimi).get(str_)


def find_template_sum(v, str_):
    if re.findall(fr'{str_}\s*(\b\d+[,.]\d{{2}}\b)', v):
        return re.findall(fr'{str_}\s*(\b\d+[,.]\d{{2}}\b)', v)[0]
    else:
        return '0,00'


def find_template_arve(v, str_):  # строка из словаря, возможный пробел, группа: непробельные символы
    #print(re.findall(fr'{str_}\s*(\S+\b)', v))
    try:
        return re.findall(fr'{str_}\s*(\S+\b)', v)[0]
    except:
        print('')
        print('*** не могу подобрать шаблон счета', v, str_)


def find_template_date(v, str_, arve_kuup='', second_=''):
    date_ = re.findall(fr'{str_}\s*(\d{{2}}\.\d{{2}}\.\d{{4}})', v)
    if date_:
        date_ = date_[0]
    else:
        days_ = int(re.findall(fr'(\d)+\s*{second_}', v)[0])
        d1 = datetime.datetime.strptime(arve_kuup, '%d.%m.%y')
        date_ = d1 + datetime.timedelta(days=days_)
        date_ = date_.strftime('%d.%m.%y')
    return my_short_date(date_)


def parse_invoice_data(arve_content, template_dict):
    arve_data = {}
    folder_dict = {}
    for k, v in arve_content.items():
        a = '!*нет шаблона'
        for t_nimi, t_v in template_dict.items():
            if t_nimi in v:
                arve_nr = find_template_arve(v, find_in_template_dict(t_nimi, 'd_arve', template_dict))
                arve_kuup = my_short_date(find_template_date(v,
                                        find_in_template_dict(t_nimi, 'd_date', template_dict)))
                arve_maks_kuup = my_short_date(find_template_date(
                    v, find_in_template_dict(t_nimi, 'd_date_maks', template_dict),
                    arve_kuup, find_in_template_dict(t_nimi, 'd_days', template_dict)))

                summa_kta = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi,
                                                                                       'd_summa_k-ta', template_dict)))
                km = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_km', template_dict)))
                total = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_total', template_dict)))

                hank_k = template_dict.get(t_nimi).get('d_konto')
                hank_s = template_dict.get(t_nimi).get('d_subschet')
                hank_subk = template_dict.get(t_nimi).get('d_subkonto')

                kul_k = template_dict.get(t_nimi).get('dkulud_konto')
                kul_s = template_dict.get(t_nimi).get('dkulud_subschet')
                kul_subk = template_dict.get(t_nimi).get('dkulud_subkonto')

                kulud = template_dict.get(t_nimi).get('d_kulud')
                komm = template_dict.get(t_nimi).get('komm')

                arvedata = namedtuple('arvedata', ['arve_nr', 'arve_kuup', 'arve_maks_kuup', 'summa_kta', 'km', 'total',
                                                   'hank_k', 'hank_s', 'hank_subk', 'kul_k', 'kul_s', 'kul_subk',
                                                   'kulud', 'komm'])
                arve_data[t_nimi] = arvedata(arve_nr, arve_kuup, arve_maks_kuup, summa_kta, km, total,
                                             hank_k, hank_s, hank_subk, kul_k, kul_s, kul_subk, kulud, komm)
                a = '*** обработано'
        folder_dict[k] = a
    return arve_data, folder_dict


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
    return df_sub


def find_subkonto_in_db(hank_subk, df_sub,
              uus_nr_comb, uus_kokku, uus_maksedate, uus_arve, uus_date, uus_kta, uus_km,
              nimi_orig, kulud, text_provodki, hank_k, hank_s, hank_subk_, kulud_k, kulud_s, kulud_subk,
              subkonto_yes, year_arve):
    nomer_subkonto = int(hank_subk.split(':')[1])
    if uus_kta + uus_km != uus_kokku:
        print('***', uus_kta + uus_km != uus_kokku)

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
        text_provodki_arve = (f'"Subconto", "6:{nomer_subkonto}:{max_nre_year}:{last_nr}","{uus_nr_comb}",,"15:1",'
                              f'"20:{uus_kokku}","21:{uus_maksedate}","25:{uus_arve}","26:{uus_date}",'
                              f'"30:{uus_date}"') + '\r\n'
    else:
        text_provodki_arve = ''

    if uus_km > 0:
        text_km = (f'"6H","{uus_date}","68","1","{hank_k}","{hank_s}","{uus_km}",'
                   f'"{nimi_orig.strip()}: {uus_nr_comb}  kaibemaks",'
                   f'"15:11","6:{nomer_subkonto}:{max_nre_year}:{last_nr}","","",""') + '\r\n'
    else:
        text_km = ''

    text_summa = (f'"6H","{uus_date}","{kulud_k}","{kulud_s}","{hank_k}","{hank_s}","{uus_kta}",'
                  f'"{nimi_orig.strip()} {uus_nr_comb}: {kulud}",'
                  f'"{kulud_subk}","6:{nomer_subkonto}:{max_nre_year}:{last_nr}","","",""')
    text_provodki += text_provodki_arve + text_km + text_summa + '\r\n'
    return text_provodki


def main():
    your_target_folder = "/Users/docha/Google Диск/Bonus/2021-09/"
    path = 'Bonus_in_arve_template.csv'
    in_or_out = 1  # 1 - входящие, 0 - исходящие

    subkonto_yes = 1  # 1 создавать новые субконто. 0 не создавать новые субконто
    year_arve = '2021'
    period_arve = f'"01.10.21","31.10.21","6H"' + '\r\n'

    r1 = re.compile(r'/\d{6}.*.pdf$')  # вводим паттерн, который будем искать (название 6 цифр +,) исходящие

    dbf = Dbf5(r'/Volumes/[C] Windows 10/Dropbox/_N/Bonus_2011/1sbspsk.dbf', codec='cp866')

    text_provodki = ''
    new_f = '/Volumes/[C] Windows 10/Dropbox/_N/Bonus_2011/BA_output_.txt'
    pdf_files = find_all_files(your_target_folder, r1, in_or_out)
    template_dict = read_csv_to_dict_template(path)
    arve_content = read_pdf_to_text_in_folder(pdf_files)

    #pprint.pprint(arve_content)

    #pprint.pprint((parse_invoice_data(arve_content, template_dict)))
    for pdf_ in pdf_files:
        print(os.path.basename(pdf_))
    #pprint.pprint(len(pdf_files))

    df_sub = read_db(dbf)
    d, fd = parse_invoice_data(arve_content, template_dict)
    #pprint.pprint(d)

    for firma, value in d.items():
        find_firma = d.get(firma)
        hank_k = find_firma.hank_k
        hank_s = find_firma.hank_s
        hank_subk_ = find_firma.hank_subk
        nimi_orig = firma

        uus_nr_comb = my_reverse_date(find_firma.arve_kuup) + ' ' + find_firma.arve_nr
        uus_kta = find_firma.summa_kta
        uus_km = find_firma.km
        uus_kokku = find_firma.total
        uus_maksedate = find_firma.arve_maks_kuup
        uus_arve = find_firma.arve_nr
        uus_date = find_firma.arve_kuup

        kulud_k = find_firma.kul_k
        kulud_s = find_firma.kul_s
        kulud_subk = find_firma.kul_subk

        kulud = find_firma.kulud

        text_provodki = find_subkonto_in_db(hank_subk_, df_sub,
                  uus_nr_comb, uus_kokku, uus_maksedate, uus_arve, uus_date, uus_kta, uus_km, nimi_orig, kulud,
                  text_provodki, hank_k, hank_s, hank_subk_, kulud_k, kulud_s, kulud_subk,
                  subkonto_yes, year_arve)


    out = f"""{period_arve}{text_provodki}"""

    pprint.pprint(fd)
    fd_ = defaultdict(list)
    for k, v in fd.items():
        fd_[v].append(k)
    pprint.pprint(fd_)

    with open(new_f, 'w') as new_f:
        new_f.write(out)
        print(out)
    #print(parse_invoice_data(arve_content).get('Elisa').summa_kta + parse_invoice_data(arve_content).get('Elisa').km)

    #"01.05.21","31.05.21","6P"
    #"Subconto", "6:144","Armina  OU",,"15:1", "91:0"
    #"Subconto", "6:144:1","2021",,
    #"Subconto", "6:144:1:2","210531 1953",,"15:1","20:20.16","21:07.06.21","23:0","25:1953","26:31.05.21","30:31.05.21"
    #"6P","31.05.21","68","1","60","1","3.36","HAE. 21018 : KM Armina OU :","15:11","6:144:1:2","","",""
    #"6P","31.05.21","26","","60","1","16.80","HAE. 21018 : Armina OU :","8:6:31","6:144:1:2","1.000","",""


if __name__ == '__main__':
    main()
