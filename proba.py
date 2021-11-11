import re
from decimal import Decimal
from collections import namedtuple
import pprint

# template_dict = {'Armina': {'d_summa_k-ta': 'Summa km-ta 20%', 'd_km': 'Käibemaks 20%',
#                             'd_total': 'Arve kokku  \(EUR\)', 'd_arve': 'Arve nr',
#                             'd_date': 'Kuupäev'},
#                  'Oculus': {'d_summa_k-ta': 'Summa ilma käibemaksuta', 'd_km': 'Käibemaks 20%',
#                             'd_total': 'Tasumisele kuulub', 'd_arve': 'ARVE NR',
#                             'd_date': 'Kuupäev:'},
#                  'Elisa': {'d_summa_k-ta': 'Summa käibemaksuta', 'd_km': 'Käibemaks \(20%\)',
#                             'd_total': 'Arve summa', 'd_arve': '100130171',
#                             'd_date': '5a-13'},
#                  'Must Have': {'d_summa_k-ta': 'Kokku maksustatav summa \(EUR\):', 'd_km': 'Käibemaks \(20%\)',
#                             'd_total': 'Kokku maksustatav summa \(EUR\):', 'd_arve': 'ARVE NR.',
#                             'd_date': 'Kuupäev:'},
#                  'Compic': {'d_summa_k-ta': 'Kokku \/ Всего', 'd_km': '20.00% Käibemaks \/VAT',
#                                'd_total': 'Summa \/ К Оплате', 'd_arve': 'Arve \/ Счет: ',
#                                'd_date': 'Kuupäev \/ Дата:'},
#                  'WAVED STRIPES': {'d_summa_k-ta': 'KOGUSUMMA', 'd_km': 'Käibemaks \(20%\)',
#                                'd_total': 'KOGUSUMMA', 'd_arve': 'ARVE - SAATELEHT Nr. ',
#                                'd_date': 'MAKSETINGIMUSED\n'},
#                  }


arve_content = {'Armina OÜ Arve nr 1953': 'Arve saaja Bonus Tõlkebüroo OÜ Arve nr 1953 '
                                                                       'Estonia pst 5-308 Kuupäev 31.05.2021 Kesklinna '
                                                                       'linnaosa, Tallinn Maksetähtpäev 07.06.2021 10143 '
                                                                       'Harju maakond Viitenumber 19538 Viivis 0.05% '
                                                                       'päevas Rg-kood 12545420 Armina oü KMKR nr '
                                                                       'EE101667290 Mõisavahe 65-15/16 50707 Tartu '
                                                                       'Rg-kood 12204073 KMKR nr EE101563815 Kirjeldus '
                                                                       'Kogus Ühik Hind Summa Pressteade 24.05.2021 1,2 '
                                                                       '14,00 16,80 Summa km-ta 20% 16,80 Käibemaks 20% '
                                                                       '3,36 Arve kokku (EUR) 20,16 Mobiil 58123444 '
                                                                       'E—post natalja.smirnova1©gmai|.com Pank SWIFT '
                                                                       'EEUHEEZX IBAN EE901010220202262225 ',
                                            'Arve Boonus 28.05.21': 'ARVE NR 2105282 \\ / \\ % OCULUS Arve saaja: '
                                                                    'Kuupäev: 28.05.2021 Bonus Tõlkebüroo OÜ Makse '
                                                                    'tähtpäev: 04.06.2021 Estonia pst 5, Tallinn 10413 '
                                                                    'KMKR: EE101667290 Arve väljastas: D. Kuznetsov '
                                                                    'Maksekorraldusele märkida arve number Tõlketeenus '
                                                                    'Faili nimi TM-de arv Lk-de arv Hind KIK toetus Tartu '
                                                                    'Millile 1072 0,60 8,34 Kinnistu servituudid 3240 '
                                                                    '1,80 25,20 Hoolduspere voldik 115,00 Kodulahe '
                                                                    'kvartal 7,00 Summa ilma käibemaksuta 155,54 € '
                                                                    'Käibemaks 20% 31,11 € Tasumisele kuulub 186,65 € '
                                                                    'Täname õigeaegselt tasutud arve eest! Oculus OÜ '
                                                                    'SEBZEE911010220223637224 Sadama 6 Та||іпп '
                                                                    'іпіо@осц|и524.ее Reg.nr.12541043 Harjumaa 10111 '
                                                                    '55569829 KMKR nr. EE101743732 ',
                                            'Arve_2123_Must_Have_Bonus': 'Must Have OÜ Registrikood: 12629464 Aadress: '
                                                                         'Mustamäe tee 78-26, Tallinn Tel. 56229011 '
                                                                         'іпіо@ти5№а\\/е.ее Bonus Tõlkebüroo OÜ Reg. nr. '
                                                                         '12545420 Estonia pst. 5-308, Tallinn 10143 ARVE '
                                                                         'NR . 2123 Kuupäev: 29.05.2021 Maksetähtaeg: '
                                                                         '12.06.2021 NIMETUS KOGUS HIND SUMMA '
                                                                         'Tõlketeenused 1397,18 1397,18 Kokku maksustatav '
                                                                         'summa (EUR): 1397,18 Saaja: Must Have OÜ '
                                                                         'Arvelduskonto: EE777700771005482091 LHV pank ',
                                            'Elisa_Teleteenuste_Arve_0521': '№ Elisa Teleteenused AS, Sõpruse pst 145, '
                                                                            '13425 Tallinn Arve number viitenumber reg nr '
                                                                            "10069659 KMKR.NR.EE100130171 JA'695739 "
                                                                            '9112106 " " " А k " A ld d OU BONUS '
                                                                            'TOLKEBUROO № ””р”" № “sarve Tedre tn 53.13 '
                                                                            '01 _052021 Swedbank EE882200001180000796 - '
                                                                            '-- - SEB Pank EE921010002046022001 KrlSlllne '
                                                                            'l|nnaosa Arve makselählaeg LHV Pank '
                                                                            'ЕЕ657700771002850697 Та|||пп Luminor Bank '
                                                                            'EE561700017000030979 11315 Harju maakond '
                                                                            '31.05.2021 Coop Pank EE484204278609841003 '
                                                                            'Laekumised 01.04.2021 kuni 30.04.2021 5594 '
                                                                            'Kreedilarved 01.04.2021 kuni 30.04.2021 0,00 '
                                                                            'Ettemaks seisuga 30.04.2021 3352 Viivis '
                                                                            '01.04.2021 kuni 30.04.2021 0,00 likud teen '
                                                                            'TEDRE TN 5A-13, TALLINN Elisa Klassik: '
                                                                            'lnternet-M + TV-LRK aprill 2021 Kuu 1 27,97 '
                                                                            '27,97 Wi-Fi teenus aprill 2021 Kuu 1 0,00 '
                                                                            '0,00 Modemi (Wi-Fi, 3.0) rent aprill 2021 '
                                                                            'Kuu 1 4,99 0,00 Т\\/ digimooduli rent aprill '
                                                                            '2021 Kuu 1 2,49 0,00 Т\\/ kaardi rent aprill '
                                                                            '2021 Kuu 1 1,99 0,00 Arve summa 27,97 '
                                                                            'Käibemaks (20%) 4,66 Summa käibemaksuta '
                                                                            '23,31 Kokku käesoleva arvega kuulub '
                                                                            'tasumisele: Arveid, laekumisi, filmi- ia '
                                                                            'kõnede erislusi Saale kõige mugavamall ia '
                                                                            'kiiremini vaadala Elisa lseleenindusesl. '
                                                                            'Täname õigeaegse“ tasutud arve eest! '
                                                                            'Klienditugi 6 600 600 www.elisa.ee Sõpruse '
                                                                            'pst 145, Tallinn '}


def my_str_to_float(str):
    # str '13,50' => float '13.5'
    return Decimal(str.replace(',', '.'))


def my_short_date(str):
    # '21.05.2021' => '21.05.21'
    return str[:6] + str[-2:]


def find_in_template_dict(t_nimi, str):
    return template_dict.get(t_nimi).get(str)


def find_template_sum(v, str):
    if re.findall(fr'{str} (\b\d+,\d{{2}}\b)', v):
        return re.findall(fr'{str} (\b\d+,\d{{2}}\b)', v)[0]
    else:
        return '0,00'


def find_template_arve(v, str):  # строка из словаря, возможный пробел, группа: непробельные символы
    return re.findall(fr'{str}\s?(\S+\b)', v)[0]


def find_template_date(v, str):
    date_ = re.findall(fr'{str} (\d{{2}}\.\d{{2}}\.\d{{4}})', v)
    return my_short_date(date_)


def parse_invoice_data():
    arve_data = {}
    for k, v in arve_content.items():
        for t_nimi, t_v in template_dict.items():
            if t_nimi in v:
                summa_kta = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_summa_k-ta')))
                km = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_km')))
                total = my_str_to_float(find_template_sum(v, find_in_template_dict(t_nimi, 'd_total')))
                arve_nr = find_template_arve(v, find_in_template_dict(t_nimi, 'd_arve'))
                arve_kuup = find_template_date(v, find_in_template_dict(t_nimi, 'd_date'))
                arvedata = namedtuple('arvedata', ['summa_kta', 'km', 'total', 'arve_nr', 'arve_kuup'])
                arve_data[t_nimi] = arvedata(summa_kta, km, total, arve_nr, arve_kuup)
    return arve_data


pprint.pprint(parse_invoice_data())
print(parse_invoice_data().get('Armina').total)

for key, values in parse_invoice_data().items():
    text_provodki = (f'"Subconto", "6:{parse_invoice_data().get(key).arve_nr}"')
    print(text_provodki)
