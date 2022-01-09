import pprint
from google.cloud import vision
import io
import os
import re

#Save the credentials file, and set its path as an environment variable
#export GOOGLE_APPLICATION_CREDENTIALS=”<path>”
#Pycharm название файла без кавычек


def find_all_jpg_files(your_target_folder):
    file_list = []
    for files_ in os.listdir(your_target_folder):
        if files_.endswith('.jpg'):
            full_path = os.path.join(your_target_folder, files_)
            file_list.append(full_path)
            file_list.sort(key=str.lower)
    return file_list


def read_jpg_to_text(file_name):
    client = vision.ImageAnnotatorClient()
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    #pprint.pprint(response)
    output = response.text_annotations[0].description
    #print(response.text_annotations[0].description)
    return output


def date_in_reciept(text):
    date_reciept = re.compile(r'''
    [0123]\d  #день
    \.        # разделитель
    [01]\d  #месяц
    \.        # разделитель
    \d{2,4}  #год
    ''', re.VERBOSE)
    kuupaev = date_reciept.search(text)
    if kuupaev:
        kuupaev = kuupaev.group()
        day_, month_, year_ = kuupaev.split('.')
        if len(year_) == 4:
            kuupaev = f'{day_}.{month_}.{year_[2:4]}'
    else:
        kuupaev = ''
    return kuupaev


def find_firm(text):
    firma_name = re.compile(r'''
    (.*(AS|OÜ|MTÜ|UÜ|FIE).*)
    ''', re.VERBOSE)
    firma_nimetus = firma_name.search(text)
    if firma_nimetus:
        firma_nimetus = firma_nimetus.group()
    else:
        firma_nimetus = ''
    return firma_nimetus


def find_pattern_from_list(text, re_list):
    for re_l in re_list:
        re_pattern = re.compile(f'{re_l}')
        re_pattern_match_ = re_pattern.search(text)
        if re_pattern_match_:
            result = re_pattern_match_.group(1)
            return result


def main():
    your_target_folder = '/Users/docha/Google Диск/Metsa10/_cheki'
    for file_name in find_all_jpg_files(your_target_folder):
        text = read_jpg_to_text(file_name)

        re_arve_list = [r'Arve nr\.\s(.*)',
                   r'SAATELEHT\s(.*)',
                   r'ARVE NR\s(.*)',
                   r'Kviitung:\s(.*)',
                   ]

        re_reg_nr_list = [r'Reg.kood\s(\b\d{8}\b)',
                r'Reg.\s*nr\.*:*\s(\b\d{8}\b)',
                r'Reg:(\d{8})']

        re_total_list = [r'KOKKU K.-ga\n(\d+[,.]\d{1,2})',
                         r'Kokku \(EUR\)\n(\d+[,.]\d{1,2})',
                         r'Kokku\n(\d+[,.]\d{1,2})',
                         r'Kokku tasutud:\n(\d+[,.]\d{1,2})',
                         r'KMX Netosumma\n.*\n.*\n(\d+[,.]\d{1,2})',
                         r'Коккu\n(\d+[,.]\d{1,2})',
                         ]

        kuupaev = date_in_reciept(text)
        firma_nimetus = find_firm(text)
        reg_nr = find_pattern_from_list(text, re_reg_nr_list)
        arve_nr = find_pattern_from_list(text, re_arve_list)
        total_sum = find_pattern_from_list(text, re_total_list)
        print(file_name)
        print('*****')
        print('kuupaev', kuupaev)
        print('firma', firma_nimetus)
        print('reg nr', reg_nr)
        print('arve nr', arve_nr)
        print('summa kokku', total_sum)
        print('*****')
        #print(text)
        print('++++')


if __name__ == '__main__':
    main()
    


