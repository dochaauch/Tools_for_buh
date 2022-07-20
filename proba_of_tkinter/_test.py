import re
from rule_template import find_firm, find_pattern_from_list
import rule_arve


text_ = '''
SIN VINTUREJE INTERNATIONAL"
17:00
18.00
SIA NNJ
RĪGA. ALEKSANDRA ČAKA IELA 55
PVN LV 40103265327
XXXXXXXXXXXXXXXXX
HKA Š/N:170802363
FM:041101188FA1
DOK. #00009568
KASIERIS 01
CITI PAKALPOJUMI 1 x 5.00
X
KOPĀ EUR
KARTE
'''

km_rate = 0.20
a = re.findall(fr'(?<!\.)(?<!\d)(\d+[,.]\d{{2}}(?!\.))', text_)
print(a)
all_digits = sorted(list(map(lambda x: float(x.replace(',', '.')), a)), reverse=True)
print(all_digits)

km_rate_list = [0.2, 0.21, 0.12]
total_sum = 0
for km_rate in km_rate_list:
    for i in all_digits:
        s = round(i / (1 + km_rate), 2)
        k = round(s * (1 + km_rate), 2)
        list_s = [round(s - 0.01, 2), s, round(s + 0.01, 2)]
        list_k = [round(k - 0.01, 2), k, round(k + 0.01, 2)]
        print(list_s)
        print(list_k)
        if any(s_ in list_s for s_ in all_digits) and any(k_ in list_k for k_ in all_digits):
            if i > 1:
                total_sum = i
                print('+++', total_sum)
                break
summa = round(total_sum / 1.2, 2)
km = round(summa * 0.2, 2)
if summa in all_digits and km in all_digits:
    print('ok')
print(total_sum, summa, km)

print('firma, внутри', find_firm(text_))
print('arve nr.', find_pattern_from_list(text_, rule_arve.re_arve_list))

text_ = re.sub(r'Klient:\s*\n*\r*\n*', 'Klient: ', text_, flags=re.MULTILINE | re.IGNORECASE)
#print(text_)
firma_name = re.compile(r'''
    (^(?:(?!Maksja:\s?|Klient:\s?|Ostja:\s?).)*?\b(AS|OÜ|MTÜ|UÜ|FIE|SIA|Osaühing|OU|Akciju)\b.*)
    ''', flags=re.VERBOSE | re.MULTILINE)
firma_nimetus = firma_name.search(text_)
#print(firma_nimetus.group())

firma_nimetus = 'Osaühing Stafit'
special_char_map = {'CÜ': 'OÜ', 'QU': 'OU', '00': 'OÜ', 'CU': 'OÜ', 'Osaühing': 'OÜ'}
for k, v in special_char_map.items():
    if firma_nimetus:
        if k in firma_nimetus:
            #print(k, firma_nimetus)
            firma_nimetus = firma_nimetus.replace(k, v)
#print('ответ', firma_nimetus)

#print('Osaühing Stafit'.replace('Osaühing', 'OÜ'))
