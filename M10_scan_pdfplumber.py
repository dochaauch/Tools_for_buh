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
import datetime
from Bonus_scan_pdfplumber import (read_csv_to_dict_template, find_all_files,
                                   read_pdf_to_text_in_folder, my_str_to_float,
                                   my_short_date, my_reverse_date,
                                   find_in_template_dict, find_template_sum,
                                   find_template_arve, find_template_date,
                                   parse_invoice_data)


def find_all_files(your_target_folder):
    file_list = []
    for files_ in os.listdir(your_target_folder):
        if files_.endswith('.pdf'):
            full_path = os.path.join(your_target_folder, files_)
            file_list.append(full_path)
            file_list.sort(key=str.lower)
    return file_list


def main():
    your_target_folder = "/Users/docha/Google Диск/Metsa10/"
    path = 'M10_in_arve_template.csv'
    in_or_out = 0  # 1 - входящие, 0 - исходящие; тут только как в образце r1

    subkonto_yes = 0  # 1 создавать новые субконто. 0 не создавать новые субконто
    year_arve = '2021'
    period_arve = f'"01.10.21","31.10.21","H1"' + '\r\n'

    r1 = re.compile(r'/.*.pdf$')  # вводим паттерн, который будем искать (все pdf)

    #dbf = Dbf5(r'/Volumes/[C] Windows 10/Dropbox/_N/Metsa10_2011/1sbspsk.dbf', codec='cp866')
    text_provodki = ''
    new_f = '/Volumes/[C] Windows 10/Dropbox/_N/Metsa10_2011/MA_output_.txt'

    pdf_files = find_all_files(your_target_folder)
    print(pdf_files)
    template_dict = read_csv_to_dict_template(path)
    pprint.pprint(template_dict)
    arve_content = read_pdf_to_text_in_folder(pdf_files)

    pprint.pprint(arve_content)

    pprint.pprint((parse_invoice_data(arve_content, template_dict)))
    for pdf_ in pdf_files:
        print(os.path.basename(pdf_))
    pprint.pprint(len(pdf_files))

    #df_sub = read_db(dbf)
    d, fd = parse_invoice_data(arve_content, template_dict)
    # pprint.pprint(d)

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
        arve_komm = find_firma.komm
        print(arve_komm)
        if arve_komm == 'komm':
            date_arve = datetime.strptime(find_firma.arve_kuup, '%d%m%y')
            first_day_of_current_month = date_arve.replace(day=1)
            date_arve = first_day_of_current_month - datetime.timedelta(days=1)
            print(date_arve)
        else:
            uus_date = find_firma.arve_kuup

        kulud_k = find_firma.kul_k
        kulud_s = find_firma.kul_s
        kulud_subk = find_firma.kul_subk

        kulud = find_firma.kulud

        text_provodki_ = (f'"H1","{uus_date}","{kulud_k}","{kulud_s}","{hank_k}","{hank_s}","{uus_kokku}",'
                  f'"{nimi_orig.strip()} {uus_nr_comb}: {kulud}",'
                  f'"{kulud_subk}","{hank_subk_}","","",""')
        print(text_provodki_)

    text_provodki += text_provodki_

    out = f"""{period_arve}{text_provodki}"""

    pprint.pprint(fd)
    fd_ = defaultdict(list)
    for k, v in fd.items():
        fd_[v].append(k)
    pprint.pprint(fd_)

    with open(new_f, 'w') as new_f:
        new_f.write(out)
        print(out)


if __name__ == '__main__':
    main()
