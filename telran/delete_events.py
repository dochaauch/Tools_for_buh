from datetime import datetime, timedelta
import chardet

start_date = "13.09.22"
end_date = "22.02.23"

s_date_object = datetime.strptime(start_date, '%d.%m.%y')
e_date_object = datetime.strptime(end_date, '%d.%m.%y')
days_ = (e_date_object - s_date_object).days

list_of_date = []
for i in range(days_ + 1):
    current_date = s_date_object + timedelta(i)
    current_date_string = current_date.strftime('%Y%m%d')
    list_of_date.append(current_date_string)

with open("my_file.ics", "rb") as fin:
    rawdata = fin.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    print(encoding)

with open("my_file.ics", "r", encoding=encoding) as fin:
    with open("changed.ics", "w") as fout:
        delete_event_flag = 0
        for line in fin:
            #for date_ in list_of_date:
                #if f'DTSTART:{date_}' not in line:
            if line.startswith('DTSTART:'):
                if not any(f'DTSTART:{date_}' in line for date_ in list_of_date):
                    delete_event_flag = 1
                    print(line, delete_event_flag)

            if "STATUS:CONFIRMED" in line and delete_event_flag == 1:
                line = "STATUS:CANCELLED" + '\n'
                print(line, delete_event_flag)
                delete_event_flag = 0
            fout.write(line)



