import csv
from decimal import Decimal
import re
import datetime
import pprint
from collections import namedtuple, defaultdict


def read_csv_to_dict_template(path):
    with open(path, newline='') as inp:
        reader = csv.DictReader(inp)
        template_dict = {row.pop('firma'): row for row in reader}
    return template_dict


def my_str_to_float(str_):
    # str_ '13,50' => float '13.5'
    return round(float(str_.replace(',', '.').replace(' ', '')), 2)


def my_short_date(str_):
    # '21.05.2021' => '21.05.21'
    return str_[:6] + str_[-2:]


def my_reverse_date(str_):
    # '21.05.2021' , '21.05.21' => 210521
    return str_[-2:] + str_[3:5] + str_[:2]


def find_in_template_dict(t_nimi, str_, template_dict):
    return template_dict.get(t_nimi).get(str_)


def find_template_sum(v, str_):
    #if re.findall(fr'{str_}\s*(\b\d+[,.]\d{{2}}\b)', v):
    #    return re.findall(fr'{str_}\s*(\b\d+[,.]\d{{2}}\b)', v)[0]
    #if re.findall(fr'{str_}\s*(\d+[,.]\d{{2}})', v):
    #    return re.findall(fr'{str_}\s*(\d+[,.]\d{{2}})', v)[0]
    if re.findall(fr'{str_}\s*([0-9 ]+\s?[,.]\s?\d{{2}})', v):
        return re.findall(fr'{str_}\s*([0-9 ]+\s?[,.]\s?\d{{2}})', v)[0]
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
    #print('arve_content')
    #pprint.pprint(arve_content)
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
                komm = template_dict.get(t_nimi).get('d_komm')

                if template_dict.get(t_nimi).get('d_vol', False):
                    print(arve_nr, template_dict.get(t_nimi).get('d_vol', False))
                    vol = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_vol', template_dict)))
                else:
                    vol = my_str_to_float('0.0')

                arvedata = namedtuple('arvedata', ['firma', 'arve_nr', 'arve_kuup', 'arve_maks_kuup', 'summa_kta', 'km', 'total',
                                                   'hank_k', 'hank_s', 'hank_subk', 'kul_k', 'kul_s', 'kul_subk',
                                                   'kulud', 'komm', 'vol'])
                #arve_data[t_nimi] = arvedata(arve_nr, arve_kuup, arve_maks_kuup, summa_kta, km, total,
                #                             hank_k, hank_s, hank_subk, kul_k, kul_s, kul_subk, kulud, komm)
                arve_data[k] = arvedata(t_nimi, arve_nr, arve_kuup, arve_maks_kuup, summa_kta, km, total,
                                             hank_k, hank_s, hank_subk, kul_k, kul_s, kul_subk, kulud, komm, vol)
                a = '*** обработано ' + arve_nr + ' ' + arve_kuup+ '/' + arve_maks_kuup + ' ' + str(total) + ' //' + str(summa_kta) + ' + ' + str(km)
        #folder_dict[k] = a
    #return arve_data, folder_dict
    return arve_data


def date_in_reciept(text):
    date_reciept = re.compile(r'''
    \b
    [0123]\d  #день
    [\.\/\\-]        # разделитель
    [01]\d  #месяц
    [\.\/\\-]        # разделитель
    \d{2,4}  #год
    ''', re.VERBOSE)

    kuupaev = date_reciept.search(text)
    if kuupaev:
        kuupaev = kuupaev.group()
        day_, month_, year_ = re.split(r'[./\-]', kuupaev)
        if len(year_) == 4:
            kuupaev = f'{day_}.{month_}.{year_[2:4]}'
        else:
            kuupaev = f'{day_}.{month_}.{year_}'
    else:
        # date_reciept2 = re.compile(r'''
        # \d{2,4}  #год
        # \-        # разделитель
        # [01]\d  #месяц
        # \-        # разделитель
        # \[0123]\d  #день
        # ''', re.VERBOSE)
        date_reciept2 = re.compile(r'\b\d{2,4}[-\/\\][01]\d[-\/\\][0123]\d', re.VERBOSE)
        kuupaev = date_reciept2.search(text)
        if kuupaev:
            kuupaev = kuupaev.group()
            year_, month_, day_ = re.split(r'[./\-]', kuupaev)
            if len(year_) == 4:
                kuupaev = f'{day_}.{month_}.{year_[2:4]}'
            else:
                kuupaev = f'{day_}.{month_}.{year_}'
        else:
            kuupaev = ''
    return kuupaev


def find_firm(text):
    #если после клиента стоит перенос строки - переносим все в одну строку
    text = re.sub(r'Klient:\s*\r*\n*', 'Klient: ', text, flags=re.IGNORECASE | re.MULTILINE)
    print(text)
    firma_name = re.compile(r'''
    (^(?:(?!Maksja: |Klient: |Ostja: ).)*
    \b(Osaühing|AS|OÜ|MTÜ|UÜ|FIE|SIA|OU|Akciju|VAS|CÜ|QU|Ühistu|00|CU|DO)\b
    .*(?<!omand)$)
    ''', flags=re.VERBOSE | re.MULTILINE )
    #(?<!,|:|.)
    firma_nimetus = ''
    #ищем кортеж вхождений
    firma_nimetus_list = firma_name.findall(text)
    if firma_nimetus_list:
        print('list', firma_nimetus_list)
        for firma_nimetus_ in firma_nimetus_list:
            fn0 = firma_nimetus_[0]
            #убираем все, что похоже на деньги, дату или время
            matches = [':00', '.00', ',00']
            if all(x not in fn0 for x in matches):
                #убираем все, что идет после запятой, считаем, что там будет адрес или пояснение
                firma_nimetus = fn0.split(',')[0]
                #убираем регистрационный номер из наименования
                firma_excl_reg = re.compile(r'(.*)(PVN|reg)', flags=re.IGNORECASE|re.VERBOSE|re.MULTILINE)
                if firma_excl_reg.search(firma_nimetus):
                    firma_nimetus = firma_excl_reg.search(firma_nimetus).group(1)
                break

    incorr_abbr = {'CÜ': 'OÜ', 'QU': 'OÜ', '00': 'OÜ', 'CU': 'OÜ', ':': '', 'OU': 'OÜ',
                   'DO': 'OÜ'}
    for k, v in incorr_abbr.items():
        if firma_nimetus:
            if k in firma_nimetus:
                firma_nimetus = firma_nimetus.replace(k, v)
    return firma_nimetus


def find_pattern_from_list(text, re_list):
    for re_l in re_list:
        re_pattern = re.compile(f'{re_l}', flags=re.IGNORECASE | re.MULTILINE)
        re_pattern_match_ = re_pattern.search(text)
        if re_pattern_match_:
            result = re_pattern_match_.group(1)
            return result

