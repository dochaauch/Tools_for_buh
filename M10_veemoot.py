#формирование файла для загрузки водомеров из эмейла Жанны
from icecream import ic
from datetime import datetime
import time
# вставить старые показатели в файл M10vana_moot.csv из произвольных отчетов последние водомеры
# вставить строку из эмейла в M10uus_moot.txt
# исправить lausendi_kuupaev


def time_format():
    return f'{datetime.now()}|> '


ic.configureOutput(prefix=time_format, includeContext=True)
#"30.04.21", "30.04.21". "VL"
#"VL", "30.04.21","VE","K1","VE","0",0.00,"VE:2104: Metsa 10-1 K1","1:1:1:2","1:3",5

lausendi_kuupaev = '31.05.22'
nr = lausendi_kuupaev.split('.')[2] + lausendi_kuupaev.split('.')[1]

first_row = f'"{lausendi_kuupaev}", "{lausendi_kuupaev}","VL"' + '\r\n'
text_provodki = ''

with open('M10uus_moot.txt', 'r') as uus_f:
    lines = uus_f.readlines()

    uus_moot = ';'.join(lines).split(';')
    uus_moot_d = dict()
    for u in uus_moot:
        k, v = u.split('-')
        k = k.strip()
        uus_moot_d[k] = float(v.strip())


with open('M10vana_moot.csv', 'r') as vana_f:
    lines = vana_f.readlines()
    for l in lines:
        vana_l = l.split(',')
        subkonto, name, aadress, vana = [s.strip() for s in vana_l]
        vana = float(vana)
        num_korter = subkonto.split(':')[2]
        if num_korter in uus_moot_d.keys():
            uus = uus_moot_d[num_korter]
            m3 = uus - vana
            if m3 < 1 or m3 > 10:
                print(num_korter, vana, uus, m3)
            text_provodki_1 = (f'"VL", "{lausendi_kuupaev}","VE","K1","VE","0",0.00,"VE:{nr}: {aadress} K1, {vana}-{uus}",'
                             f'"{subkonto}","1:3",{m3}')
            text_provodki += text_provodki_1 + '\r\n'

out = first_row + text_provodki
print()
print(out)
v = open('/Volumes/[C] Windows 10 (1)/Dropbox/_N/Metsa10_2011/veemotjad.txt', 'w')

v.write(out)
v.close()