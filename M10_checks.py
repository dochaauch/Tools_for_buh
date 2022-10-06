from datetime import datetime

file_ = '/Users/docha/Google Диск/Metsa10/_cheki/combine.csv'
#file_ = '/Users/docha/Google Диск/Metsa10/1/combine.csv'

today = datetime.now()
stamp = today.strftime('%y%m%d')

text_provodki = ''
date_list = []

with open(file_, 'r') as csv_file:
    lines = csv_file.readlines()[1:]

    for l in lines:
        linie = l.split(',')
        n, kuupaev, firma, regnr, arve_nr, summa_ilma, km, summa, kirjeldus, auto, *oth =\
                [s.strip() for s in linie]
        nr = kuupaev.split('.')[2] + kuupaev.split('.')[1]
        text_provodki_1 = (f'"AV", "{kuupaev}","21","","71","02",{summa},"{stamp} AV:{nr} {firma} {arve_nr} {kirjeldus}", '
                           f'"5:1:20","2:4",""')
        text_provodki += text_provodki_1 + '\r\n'
        date_ = datetime.strptime(kuupaev, '%d.%m.%y')

        date_list.append(date_)

min_date = min(date_list)
min_date = datetime.strftime(min_date, '%d.%m.%y')
max_date = max(date_list)
max_date = datetime.strftime(max_date, '%d.%m.%y')

first_row = f'"{min_date}", "{max_date}","AV"' + '\r\n'

out = first_row + text_provodki
special_char_map = {ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
                            ord('ž'): 'z', ord('š'): 's',
                            ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
                            ord('Z'): 'Z', ord('Š'): 's', ord('’'): ''}
out = out.translate(special_char_map)
print()
print(out)
v = open('/Volumes/[C] Windows 10 (1)/Dropbox/_N/Metsa10_2011/avanss.txt', 'w')


v.write(out)
v.close()
