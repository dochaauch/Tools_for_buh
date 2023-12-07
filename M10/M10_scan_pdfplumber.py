from collections import defaultdict
import re
import os
import pprint
import datetime
from Bonus.Bonus_scan_pdfplumber import (read_csv_to_dict_template, find_all_files,
                                         read_pdf_to_text_in_folder, my_reverse_date,
                                         parse_invoice_data)

import Bonus.without_umlaut


def find_all_files(your_target_folder):
    file_list = []
    for files_ in os.listdir(your_target_folder):
        if files_.endswith('.pdf'):
            full_path = os.path.join(your_target_folder, files_)
            file_list.append(full_path)
            file_list.sort(key=str.lower)
    return file_list


def main():
    your_target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10"
    path = 'M10_in_arve_template.csv'
    in_or_out = 0  # 1 - входящие, 0 - исходящие; тут только как в образце r1

    subkonto_yes = 0  # 1 создавать новые субконто. 0 не создавать новые субконто
    year_arve = '2023'
    begin_date = '01.11.23'
    end_date = '30.11.23'
    period_arve = f'{begin_date},{end_date},"H1"' + '\r\n'



    r1 = re.compile(r'/.*.pdf$')  # вводим паттерн, который будем искать (все pdf)

    #dbf = Dbf5(r'/Volumes/[C] Windows 10/Dropbox/_N/Metsa10_2011/1sbspsk.dbf', codec='cp866')
    text_provodki = ''
    #new_f = '/Volumes/[C] Windows 10 (1)/Dropbox/_N/Metsa10_2011/MA_output_.txt'
    new_f = '/Users/docha/Library/CloudStorage/Dropbox/_N/Metsa10_2011/MA_output_.txt'

    pdf_files = find_all_files(your_target_folder)
    template_dict = read_csv_to_dict_template(path)
    #pprint.pprint(template_dict)
    arve_content = read_pdf_to_text_in_folder(pdf_files)


    pprint.pprint(arve_content)

    #pprint.pprint((parse_invoice_data(arve_content, template_dict)))
    for pdf_ in pdf_files:
        print(os.path.basename(pdf_))
    print('количество файлов в папке', len(pdf_files))

    #df_sub = read_db(dbf)
    d, fd = parse_invoice_data(arve_content, template_dict)
    pprint.pprint(d)

    for firma, value in d.items():
        find_firma = d.get(firma)
        hank_k = find_firma.hank_k
        hank_s = find_firma.hank_s
        hank_subk_ = find_firma.hank_subk
        nimi_orig = firma
        #print('###', find_firma.arve_nr, find_firma.arve_kuup)
        uus_nr_comb = my_reverse_date(find_firma.arve_kuup) + ' ' + find_firma.arve_nr
        uus_kta = find_firma.summa_kta
        uus_km = find_firma.km
        uus_kokku = find_firma.total
        uus_maksedate = find_firma.arve_maks_kuup
        uus_arve = find_firma.arve_nr
        arve_komm = find_firma.komm

        if arve_komm == 'komm' and int(find_firma.arve_kuup[:2]) < 10:
            date_arve = datetime.datetime.strptime(find_firma.arve_kuup, '%d.%m.%y')
            first_day_of_current_month = date_arve.replace(day=1)
            uus_date = first_day_of_current_month - datetime.timedelta(days=1)
            uus_date = uus_date.strftime('%d.%m.%y')
        else:
            uus_date = find_firma.arve_kuup

        kulud_k = find_firma.kul_k
        kulud_s = find_firma.kul_s
        kulud_subk = find_firma.kul_subk

        kulud = find_firma.kulud
        if find_firma.vol != 0:
            arve_vol = find_firma.vol
            arve_tariif = round(uus_kokku / find_firma.vol, 6)
        else:
            arve_vol = ''
            arve_tariif = ''
        nl = '\r\n'
        text_provodki_ = (f'"H1","{uus_date}","{kulud_k}","{kulud_s}","{hank_k}","{hank_s}","{uus_kokku}",'
                  f'"{find_firma.firma} {uus_nr_comb}: {kulud} {arve_vol} {arve_tariif}",'
                  f'"{kulud_subk}","{hank_subk_}","","",""{nl}')


        text_provodki += text_provodki_

    raamat_arve = (f'"H1","{end_date}","21","","76","","76.80",'
                  f'"Jakobson Jelena FIE {my_reverse_date(end_date)}: raamatupidamine",'
                  f'"5:3:1","3:4","","",""{nl}')


    out = f"""{period_arve}{raamat_arve}{text_provodki}"""
    out = Bonus.without_umlaut.translateString(out)

    #pprint.pprint(fd)
    fd_ = defaultdict(list)
    for k, v in fd.items():
        fd_[v].append(k)
    #pprint.pprint(fd_)

    with open(new_f, 'w') as new_f:
        new_f.write(out)
        print(out)


if __name__ == '__main__':
    main()
