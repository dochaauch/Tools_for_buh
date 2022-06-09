import pickle
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import fitz
import pprint
from google.cloud import vision
import io
import re
import os
from proba_to_read_check import date_in_reciept, find_firm, find_pattern_from_list, my_reverse_date, \
    my_short_date, my_str_to_float

from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter.font as font
import pandas as pd
import datetime



i_file = 0
your_target_folder = r'/Users/docha/Google Диск/Metsa10/_cheki'
#file_ = r'/Users/docha/Google Диск/Metsa10/_cheki/211106_0812_Файл_000.jpg'

list_of_files = [fn for fn in os.listdir(your_target_folder)
                  if any(fn.endswith(ext) for ext in ['.jpg',])]

system_text = ''
km_rate = '0.2'
#если для windows, то поставить w, иначе m
which_os = 'm'

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global your_target_folder, list_of_files
    filename = filedialog.askdirectory()
    your_target_folder = filename
    list_of_files = [fn for fn in os.listdir(your_target_folder)
                  if any(fn.endswith(ext) for ext in ['.jpg',])]
    load_data(i_file, list_of_files, your_target_folder)


class PDFViewer(ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') # clear current content
        pdf = fitz.open(pdf_file) # open the PDF file
        self.images = []   # for storing the page images
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)


def load_data(i_file, list_of_files, your_target_folder):
    file_ = f'{your_target_folder}/{list_of_files[i_file]}'


    # pdf field
    pdf1 = PDFViewer(root, width=70, height=25, spacing3=5, bg='blue')
    pdf1.grid(row=0, column=0, sticky='nsew')
    pdf1.show(file_)

    # raw text field
    raw_text_output = read_jpg_to_text(file_)
    display_textbox(raw_text_output, 0, 1, root, 40, 70)

    # output text field label
    output_text = tk.StringVar()
    output_img = tk.Label(root, textvariable=output_text, font=("shanti", 14))
    output_text.set('Результат сканирования')
    output_img.grid(row=2, column=0)

    # output text field
    file_pkl = f'{os.path.splitext(file_)[0]}.pkl'
    if os.path.exists(file_pkl):
        output_text, system_text = read_dict_from_file(file_pkl)
    else:
        output_text = processing_text(raw_text_output)
        system_text = f'файл {file_} для изображения {i_file + 1} ТОЛЬКО ОТСКАНИРОВАН'
    output_textbox = display_textbox(output_text, 3, 0, root, 8, 70)

    #system text
    system_text_field(system_text, root)

    # текст между стрелками
    what_text = tk.StringVar()
    what_img = tk.Label(root, textvariable=what_text, font=("shanti", 11))
    what_text.set(f'image {i_file + 1} of {str(len(list_of_files))}')
    what_img.grid(row=2, column=3)

    # arrow buttons
    display_icon('arrow_l.png', 2, 2, 'E', lambda: left_arrow())
    display_icon('arrow_r.png', 2, 4, 'W', lambda: right_arrow())

    # button save
    save_text = tk.StringVar()
    save_btn = tk.Button(root, textvariable=save_text,
                           command=lambda:save_dict_to_file(output_textbox.get("1.0", "end-1c")),
                           font=myFont,
                           highlightbackground='yellow', fg="blue", height=1,
                           width=15, borderwidth=4, relief="ridge")
    save_text.set("Save")
    save_btn.grid(column=2, row=3, sticky='nw', padx=50, columnspan=3)

    # button to_csv
    csv_text = tk.StringVar()
    csv_btn = tk.Button(root, textvariable=csv_text,
                           command=lambda:dict_to_csv(your_target_folder,'.pkl'),
                           font=myFont,
                           highlightbackground='yellow', fg="blue", height=1,
                           width=15, borderwidth=4, relief="ridge")
    csv_text.set("save to csv")
    csv_btn.grid(column=2, row=4, sticky='nw', padx=50, columnspan=3)


def system_text_field(system_text, root):
    # system text field label
    sys_text = tk.StringVar()
    sys_img = tk.Label(root, textvariable=sys_text, font=("shanti", 14))
    sys_text.set('Системные сообщения')
    sys_img.grid(row=2, column=1)

    # system text field
    sys_text = system_text
    display_textbox(sys_text, 3, 1, root, 8, 70)


def load_dict_from_file(file_name):
    with open(file_name, 'rb') as file_dict:
        output_dict = pickle.load(file_dict)
        return output_dict


def dict_to_csv(your_target_folder, exten):
    #your_target_folder = r'/Users/docha/Google Диск/Metsa10/_cheki'
    list_of_files = [fn for fn in os.listdir(your_target_folder)
                      if any(fn.endswith(ext) for ext in [exten,])]
    list_of_dict = []

    for file_ in list_of_files:
        a = load_dict_from_file(os.path.join(your_target_folder, file_))
        filename, fileextension = os.path.splitext(file_)
        b = f'=HYPERLINK("{filename}.jpg","{filename}.jpg")'
        a['file_name'] = b
        list_of_dict.append(a)

    df = pd.DataFrame(list_of_dict)
    df["summa kokku"] = pd.to_numeric(df["summa kokku"])
    df["summa"] = pd.to_numeric(df["summa"])
    df["km"] = pd.to_numeric(df["km"])
    print(df.to_string())
    df.to_excel(f'{your_target_folder}/combine.xlsx')
    df.to_csv(f'{your_target_folder}/combine.csv')
    system_text = f'CSV файл {your_target_folder}/combine.csv сохранен'
    system_text_field(system_text, root)


def right_arrow():
    global i_file
    if i_file < len(list_of_files) - 1:
        i_file += 1
    else:
        i_file = 0
    load_data(i_file, list_of_files, your_target_folder)
    return i_file


def left_arrow():
    global i_file
    if i_file == 0:
        i_file = len(list_of_files) - 1
    else:
        i_file -= 1
    load_data(i_file, list_of_files, your_target_folder)
    return i_file


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


def save_dict_to_file(output):
    global system_text
    global list_of_files
    file_ = f'{your_target_folder}/{list_of_files[i_file]}'
    filename, file_extension = os.path.splitext(file_)
    dict_data = {}
    for line_ in output.splitlines():
        key, value = line_.split(': ')
        dict_data[key] = value
    if which_os == 'w':
        file_date_ = os.path.getctime(file_)
    else:
        file_date_ = os.stat(file_).st_birthtime
    file_date = datetime.datetime.fromtimestamp(file_date_).strftime('%y%m%d_%H%M')
    new_filename = f"{my_reverse_date(dict_data['kuupaev'])}_{dict_data['firma']}_{dict_data['arve nr']}_{file_date}"

    special_char_map = {ord('/'): '-', ord('"'): '', }
    new_filename = new_filename.translate(special_char_map)

    #print(new_filename)
    list_of_files[i_file] = f'{new_filename}.jpg'
    os.rename(file_, f'{your_target_folder}/{new_filename}.jpg')
    dict_file = f'{your_target_folder}/{new_filename}.pkl'
    system_text = f'Файл {your_target_folder}/{new_filename}.pkl для изображения {i_file + 1} сохранен.'
    with open(dict_file, 'wb') as pickle_file:
        pickle.dump(dict_data, pickle_file)

    system_text_field(system_text, root)


def read_dict_from_file(file_pkl):
    global system_text
    system_text = f'Файл {file_pkl} для изображения {i_file + 1} прочитан.'
    system_text_field(system_text, root)
    d = load_dict_from_file(file_pkl)
    d_list = [str(k) + ': ' + str(v) for k, v in d.items()]
    s_ = '\n'.join(d_list)
    return s_, system_text


def display_textbox(content, ro, col, root, height, width):
    text_box = tk.Text(root, height=height, width=width, padx=5, pady=0)
    text_box.insert(1.0, content)
    text_box.tag_configure("left", justify="left")
    text_box.tag_add("left", 1.0, "end")
    text_box.grid(column=col, row=ro, sticky='nw', padx=0, pady=0)
    return text_box


def display_icon(url, row, column, stick, funct):
    icon = Image.open(url)
    icon = icon.resize((20,20))
    icon = ImageTk.PhotoImage(icon)
    icon_label = tk.Button(image=icon, command=funct, width=25, height=25)
    icon_label.image = icon
    icon_label.grid(column=column, row=row, sticky=stick)


def processing_text(text):
    re_arve_list = [r'Arve nr\.\s(.*)',
                    r'SAATELEHT\s(.*)',
                    r'ARVE NR\s(.*)',
                    r'Arve\s*(.*)',
                    r'Arve-Saateleht nr.:\s(.*)',
                    r'Kviitung:\s(.*)',
                    r'Sularahaarve nr.\s(.*)',
                    r'TSEKK/ARVE\s(.*)',
                    r'Saateleht-arve nr. (.*)',
                    r'Ceks (.*)',
                    r'čeks (.*)',
                    ]

    re_reg_nr_list = [r'Reg.kood\s(\b\d{8}\b)',
                      r'Reg.\s*nr\.*:*\s(\b\d{8}\b)',
                      r'Reg:(\d{8})',
                      r'REG.NR.:(\d{8})',
                      r'Registrikood:\s*(\d{8})'
                      ]

    re_total_list = [r'KOKKU K.-ga\n(\d+[,.]\d{1,2})',
                     r'Kokku \(EUR\)\n(\d+[,.]\d{1,2})',
                     r'Kokku\n(\d+[,.]\d{1,2})',
                     r'Kokku tasutud:\n(\d+[,.]\d{1,2})',
                     r'KMX Netosumma\n.*\n.*\n(\d+[,.]\d{1,2})',
                     r'Коккu\n(\d+[,.]\d{1,2})',
                     r'Kokku € (\d+[,.]\d{1,2})',
                     r'KOKKU EUR\n(\d+[,.]\d{1,2})',
                     r'Summa kokku:\n(\d+[,.]\d{1,2})',
                     r'KOKKU\n(\d+[,.]\d{1,2})',
                     ]

    re_sum_list = [r'Kokku ilma käibemaksuta:\n(\d+[,.]\d{1,2})',
                   r'KOKKU KM-ta\n(\d+[,.]\d{1,2})',
                   r'KAIBEMAKSUTA\n(\d+[,.]\d{1,2})',
                   r'Netosumma (20%) € (\d+[,.]\d{1,2})',
                   r'KÄIBEMAKSUTA\n(\d+[,.]\d{1,2})',
                   ]

    re_km_list = [r'Käibemaks 20%:\n(\d+[,.]\d{1,2})',
                  r'Käibemaks 20 %\n(\d+[,.]\d{1,2})',
                  r'KM %\n(\d+[,.]\d{1,2})',
                  r'Käibemaks (20%) (\d+[,.]\d{1,2})',
                  r'Käibemaks kokku\n(\d+[,.]\d{1,2})',
                  ]

    kuupaev = date_in_reciept(text)
    if kuupaev:
        kuupaev = my_short_date(kuupaev)
    firma_nimetus = find_firm(text)
    reg_nr = find_pattern_from_list(text, re_reg_nr_list)
    arve_nr = find_pattern_from_list(text, re_arve_list)

    total_sum = find_pattern_from_list(text, re_total_list)
    if total_sum:
        total_sum = my_str_to_float(total_sum)
    if not total_sum:
        total_sum = 0

    arve_sum = find_pattern_from_list(text, re_sum_list)
    if arve_sum:
        arve_sum = my_str_to_float(arve_sum)
    if not arve_sum and total_sum:
        arve_sum = round(total_sum / (1 + my_str_to_float(km_rate)), 2)
    if arve_sum != round(total_sum / (1 + my_str_to_float(km_rate)), 2):
        arve_sum = round(total_sum / (1 + my_str_to_float(km_rate)), 2)

    arve_km = find_pattern_from_list(text, re_km_list)
    if arve_km:
        arve_km = my_str_to_float(arve_km)
    if not arve_km and total_sum:
        arve_km = round(total_sum / (1 + my_str_to_float(km_rate)) * my_str_to_float(km_rate), 2)
    if arve_km != round(total_sum / (1 + my_str_to_float(km_rate)) * my_str_to_float(km_rate), 2):
        arve_km = round(total_sum / (1 + my_str_to_float(km_rate)) * my_str_to_float(km_rate), 2)

    nl = '\n'
    output = f'kuupaev: {kuupaev}{nl}' \
             f'firma: {firma_nimetus}{nl}' \
             f'reg nr: {reg_nr}{nl}' \
             f'arve nr: {arve_nr}{nl}' \
             f'summa: {arve_sum}{nl}' \
             f'km: {arve_km}{nl}' \
             f'summa kokku: {total_sum}{nl}' \
             f'kirjeldus: {nl}' \
             f'auto: {nl}'
    return output



root = tk.Tk()
root.rowconfigure((0,1), weight=1)
root.columnconfigure((0,1), weight=1)

myFont = font.Font(family='Raleway', size=14, weight='bold', slant="italic")


#button browse
browse_text = tk.StringVar()
#browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda:browse_button(),
                       font=myFont, highlightbackground='yellow', fg="blue", height=1, width=15,)
browse_text.set("Browse")
browse_btn.grid(column=2, row=1, sticky='nw', padx=50, columnspan=3)



root.mainloop()
