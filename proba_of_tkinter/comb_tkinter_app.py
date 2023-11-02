import pickle
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import fitz
import pprint
from google.cloud import vision
import io
import re
import os
from icecream import ic
import json


from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter.font as font
import pandas as pd
from tabulate import tabulate
import datetime
import csv

import rule_arve
import rule_reg
import rule_total
import rule_sum
import rule_km
from rule_template import (read_csv_to_dict_template, my_str_to_float, my_short_date, my_reverse_date,
                           find_in_template_dict, find_template_sum, find_template_arve, find_template_date,
                           parse_invoice_data,
                           date_in_reciept, find_firm, find_pattern_from_list, find_arve_pattern_from_list)

from funct import create_toler_list, find_total_sum_km, find_km_no_sum, find_sum_no_km, take_only_total, find_if_no_km_or_sum



i_file = 0  #номер изображения
jpg_nr = 0
your_target_folder = r'/Users/docha/Google Диск/Metsa10/_cheki'
your_target_folder = r'/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Metsa10/_cheki'
template_path = r'/Users/docha/PycharmProjects/Tools_for_buh/proba_of_tkinter/rule_arve_template.csv'
#file_ = r'/Users/docha/Google Диск/Metsa10/_cheki/211106_0812_Файл_000.jpg'


def time_format():
    return f'{datetime.datetime.now()}|> '
ic.configureOutput(prefix=time_format, includeContext=True)

list_of_files = [fn for fn in os.listdir(your_target_folder)
                  if any(fn.endswith(ext) for ext in ['.jpg',])]

system_text = ''
raw_text_output = ''
output_text_first = ''

km_rate_list = [0.2, 0.21, 0.09, 0.12, 0.19]


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global your_target_folder, list_of_files
    filename = filedialog.askdirectory()
    your_target_folder = filename
    list_of_files = sorted([fn for fn in os.listdir(your_target_folder)
                  if any(fn.endswith(ext) for ext in ['.jpg',])])
    load_data(i_file, list_of_files, your_target_folder, root)


class PDFViewer(ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = []
        self.original_images = []  # for storing the original images
        self.zoom_level = 100  # initial zoom level in percentage


    def show(self, pdf_file):
        print(pdf_file)
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
            self.original_images.append((photo, pix1.tobytes('ppm')))  # Save the original image data

    def zoom_in(self):
        self.zoom_level += 10
        print("zoom in", self.zoom_level)
        self.update_zoom()

    def zoom_out(self):
        self.zoom_level -= 10
        print("zoom out", self.zoom_level)
        self.update_zoom()

    def update_zoom(self):
        self.delete('1.0', 'end')  # clear current content
        self.images = []  # clear current images
        for photo, data in self.original_images:
            # Get the image from the original data
            img = Image.open(io.BytesIO(data))
            img = img.resize((int(img.width * self.zoom_level / 100), int(img.height * self.zoom_level / 100)))
            photo = ImageTk.PhotoImage(img)
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)

    def on_key_press(self, event):
        if event.keysym == "plus":
            self.zoom_in()
        elif event.keysym == "minus":
            self.zoom_out()
        # Call the superclass method to handle other key events
        super().event_generate("<<KeyPress>>", when="tail")


def load_data(i_file, list_of_files, your_target_folder, root):
    global raw_text_output
    global system_text
    global output_text_first
    file_ = f'{your_target_folder}/{list_of_files[i_file]}'

    # pdf field
    pdf1 = PDFViewer(root, width=70, height=25, spacing3=5, bg='blue')
    pdf1.grid(row=0, column=0, sticky='nsew')
    pdf1.show(file_)

    def zoom_in(event):
        pdf1.zoom_in()

    def zoom_out(event):
        pdf1.zoom_out()

    root.bind('<KeyPress-plus>', zoom_in)
    root.bind('<KeyPress-minus>', zoom_out)

    # raw text field
    file_txt = f'{os.path.splitext(file_)[0]}.ocr'
    nl = '\n\n'
    if os.path.exists(file_txt):
        raw_text_output, s_text = read_text_from_file(file_txt)
        system_text += nl + s_text
    else:
        raw_text_output = read_jpg_to_text(file_)
    text_box = display_textbox(raw_text_output, 0, 1, root, 40, 70)

    # output text field label
    output_text = tk.StringVar()
    output_img = tk.Label(root, textvariable=output_text, font=("shanti", 14))
    output_text.set('Результат сканирования')
    output_img.grid(row=2, column=0)

    # output text field
    file_pkl = f'{os.path.splitext(file_)[0]}.pkl'
    nl = '\n\n'
    if os.path.exists(file_pkl):
        output_text, s_text = read_dict_from_file(file_pkl)
        nl = '\n\n'
    else:
        output_text = processing_text(raw_text_output)

        s_text = f'файл {file_} для изображения {i_file + 1} ТОЛЬКО ОТСКАНИРОВАН'
    output_text_first = output_text
    system_text += nl + s_text
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

    # поле для ввода номера изображения
    jpg_nr_textbox = display_textbox(i_file, 0, 4, root, 5, 5)

    # button jpg nr
    jpg_nr_text = tk.StringVar()
    jpg_nr_btn = tk.Button(root, textvariable=jpg_nr_text,
                           command=lambda:select_nr_jpg(select_nr_jpg(jpg_nr_textbox.get("1.0", "end-1c"))),
                           font=myFont,
                           highlightbackground='yellow', fg="blue", height=1,
                           width=15, borderwidth=4, relief="ridge")
    jpg_nr_text.set("select nr img")
    jpg_nr_btn.grid(column=2, row=0, sticky='nw', padx=25, columnspan=2)

    # create an Entry widget for the search key
    search_entry = tk.Entry(root)
    search_entry.grid(row=1, column=1, sticky='nw')  # adjust the position as needed

    # bind the Entry widget to the search function
    search_entry.bind('<Return>', lambda event: search_text(event, text_box, search_entry))


def search_text(event, text_box, search_entry):
    # remove any existing tags from previous searches
    text_box.tag_remove('found', '1.0', tk.END)

    # get the search key
    s = search_entry.get()

    if s:
        idx = '1.0'
        while True:
            idx = text_box.search(s, idx, nocase=1, stopindex=tk.END)
            if not idx: break

            lastidx = '%s+%dc' % (idx, len(s))

            # tag the found text
            text_box.tag_add('found', idx, lastidx)
            idx = lastidx

        # configure the tag
        text_box.tag_config('found', foreground='red')



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
        return pickle.load(file_dict)


def load_text_from_file(file_name):
    with open(file_name, 'r') as file_text:
        return file_text.read()


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
    print("Вывод не обработанной таблицы,без перевода в числовые значения")
    print(tabulate(df))
    df["summa kokku"] = pd.to_numeric(df["summa kokku"])
    df["summa"] = pd.to_numeric(df["summa"])
    df["km"] = pd.to_numeric(df["km"])
    print("Вывод того,что сохраняется в csv, уже обработанный")
    print(df.to_string())
    df.to_excel(f'{your_target_folder}/combine.xlsx')
    df.to_csv(f'{your_target_folder}/combine.csv')
    system_text = f'CSV файл {your_target_folder}/combine.csv сохранен'
    system_text_field(system_text, root)


def select_nr_jpg(jpg_nr_):
    global i_file
    global system_text
    global jpg_nr
    i_file, jpg_nr = int(jpg_nr_), int(jpg_nr_)
    system_text = ''
    load_data(i_file, list_of_files, your_target_folder)
    return i_file


def right_arrow():
    global i_file
    global system_text
    if i_file < len(list_of_files) - 1:
        i_file += 1
    else:
        i_file = 0
    system_text = ''
    load_data(i_file, list_of_files, your_target_folder)
    return i_file


def left_arrow():
    global i_file
    global system_text
    if i_file == 0:
        i_file = len(list_of_files) - 1
    else:
        i_file -= 1
    system_text = ''
    load_data(i_file, list_of_files, your_target_folder)
    return i_file



def read_jpg_to_text(file_name):
    client = vision.ImageAnnotatorClient()
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    #pprint.pprint(response)
    #print(response.text_annotations[0].description)
    return response.text_annotations[0].description


def convert_timestamp_(time_, format_='%y%m%d_%H%M'):
    return datetime.datetime.fromtimestamp(time_).strftime(format_)


def save_dict_to_file(output):
    global system_text
    global list_of_files
    global raw_text_output
    global output_text_first
    file_ = f'{your_target_folder}/{list_of_files[i_file]}'
    filename, file_extension = os.path.splitext(file_)
    ic(file_, filename, file_extension)

    dict_data = {}
    dict_of_changes = {}
    first_dict = {}

    for line_ in output.splitlines():
        key, value = line_.split(': ', 1)
        dict_data[key] = value
    dict_data['not_changed'] = dict_data.get('not_changed', 'yes')
    dict_data['change_log'] = dict_data.get('change_log', dict_of_changes)

    if dict_data['change_log']:
        dict_of_changes = json.loads(dict_data['change_log'].replace("'", '"'))
    #dict_data['not_changed'] = 'yes'
    #dict_data['change_log'] = dict_of_changes


    needed_fields = ['kuupaev', 'firma', 'reg nr', 'arve nr', 'summa', 'km', 'summa kokku', ]
    for line in output_text_first.splitlines():
        k, v = line.split(': ', 1)
        if k in needed_fields:
            first_dict[k] = v

    #сверяем с первоначальным вводом
    for k, v in first_dict.items():
        if dict_data[k] != first_dict[k]:
            dict_data['not_changed'] = 'no'
            dict_of_changes[k] = [first_dict[k], dict_data[k]]


    list_of_times = [os.path.getmtime(file_),
                     os.path.getctime(file_),
                     os.stat(file_).st_birthtime]
    file_date = convert_timestamp_(min(filter(None, list_of_times)))

    new_filename = f"{my_reverse_date(dict_data['kuupaev'])}_{dict_data['firma']}_{dict_data['arve nr']}_{file_date}"

    special_char_map = {ord('/'): '-', ord('"'): '', }
    new_filename = new_filename.translate(special_char_map)

    #print(new_filename)
    #ic(list_of_files)
    list_of_files[i_file] = f'{new_filename}.jpg'
    os.rename(file_, f'{your_target_folder}/{new_filename}.jpg')

    if os.path.exists(f'{filename}.ocr'):
        os.remove(f'{filename}.ocr')
    if os.path.exists(f'{filename}.pkl'):
        os.remove(f'{filename}.pkl')

    dict_file = f'{your_target_folder}/{new_filename}.pkl'
    text_file = f'{your_target_folder}/{new_filename}.ocr'
    system_text = f'Файл {your_target_folder}/{new_filename}.pkl и файл ' \
                  f'{your_target_folder}/{new_filename}.ocr для изображения {i_file + 1} сохранен.'
    with open(dict_file, 'wb') as pickle_file:
        pickle.dump(dict_data, pickle_file)

    with open(text_file, 'w') as text_f:
        text_f.writelines(raw_text_output)

    system_text_field(system_text, root)


def read_dict_from_file(file_pkl):
    #global system_text
    s_text = f'Файл {file_pkl} для изображения {i_file + 1} прочитан.'
    #system_text_field(system_text, root)
    d = load_dict_from_file(file_pkl)
    d_list = [str(k) + ': ' + str(v) for k, v in d.items()]
    s_ = '\n'.join(d_list)
    return s_, s_text


def read_text_from_file(file_txt):
    #global system_text
    s_text = f'Файл {file_txt} для изображения {i_file + 1} загружен.'
    #system_text_field(system_text, root)
    s_ = load_text_from_file(file_txt)
    return s_, s_text


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


def check_if_template_or_regexp(text):
    template_dict = read_csv_to_dict_template(template_path)
    for templ_key in template_dict.keys():
        if templ_key in text:
            return 'template'
        else:
            return 'regexp'


def processing_text(text):
    check_temp_reg = check_if_template_or_regexp(text)
    if check_temp_reg == 'template':
        template_dict = read_csv_to_dict_template(template_path)
        arve_data = parse_invoice_data(text, template_dict)
        nl = '\n'
        output = f'kuupaev: {arve_data.arve_kuup}{nl}' \
                 f'firma: {arve_data.firma}{nl}' \
                 f'reg nr: {nl}' \
                 f'arve nr: {arve_data.arve_nr}{nl}' \
                 f'summa: {arve_data.summa_kta}{nl}' \
                 f'km: {arve_data.km}{nl}' \
                 f'summa kokku: {arve_data.total}{nl}' \
                 f'kirjeldus: {nl}' \
                 f'auto: {nl}'
    else:
        output = processing_text_regexp(text)
    return output


def processing_text_regexp(text):
    #подключаем правила-списки для регулярных выражений
    re_arve_list = rule_arve.re_arve_list

    re_reg_nr_list = rule_reg.re_reg_nr_list

    re_arve_name = rule_arve.re_arve_name

    #re_total_list = rule_total.re_total_list

    #re_sum_list = rule_sum.re_sum_list

    #re_km_list = rule_km.re_km_list

    kuupaev = date_in_reciept(text)
    if kuupaev:
        kuupaev = my_short_date(kuupaev)

    firma_nimetus = find_firm(text)
    if firma_nimetus:
        firma_nimetus = firma_nimetus.replace(':', ' ')
    reg_nr = find_pattern_from_list(text, re_reg_nr_list)
    #arve_nr = find_pattern_from_list(text, re_arve_list)
    arve_nr = find_arve_pattern_from_list(text, re_arve_name, rule_arve.list_not_arve,
                                          rule_arve.arve_exclude_list)
    if arve_nr:
        arve_nr = arve_nr.replace(':', ' ')

    a = re.findall(fr'(?<!\.)(?<!\d)([0-9]+\s?[,.]\d{{2}}(?!\.))', text)
    # впереди нет точки и цифра (пытаемся исключить дату)
    # (\d+[,.]\d{{2}} => одна или несколько цифр, запятая или точка, 2 цифры
    # если после не идет точка (пытаемся исключить дату)
    # собираем список всех цифр в нужном формате из текста
    try:
        all_digits = sorted(list(map(lambda x: float(x.replace(',', '.').replace(' ', '')), a)), reverse=True)
    except:
        all_digits = list()
    print('all_digits', all_digits)

    flag_total = False
    #пытаемся нормально подобрать сумму и налог
    total_sum, arve_sum, arve_km = find_total_sum_km(all_digits, km_rate_list)
    #если не получилось - находим налог и общую сумму
    if total_sum == 0:
        #total_sum, arve_sum, arve_km = find_km_no_sum(all_digits, km_rate_list)
        total_sum, arve_sum, arve_km = find_if_no_km_or_sum(all_digits, km_rate_list)
    #если не получилось - находим всего и высчитываем налог
    #if total_sum == 0:
    #    total_sum, arve_sum, arve_km = find_sum_no_km(all_digits, km_rate_list)
    #если ничего подобрать не получилось - считаем total максимальной суммой
    if total_sum == 0:
        total_sum = take_only_total(all_digits)

    if total_sum != 0:
        flag_total = True


    if total_sum != arve_sum + arve_km and total_sum - (arve_sum + arve_km) < 0.02:
        arve_sum += total_sum - (arve_sum + arve_km)
        arve_sum = round(arve_sum, 2)

    #если на счете только одна единственная сумма
    if len(all_digits) < 2:
        try:
            total_sum = all_digits[0]
            flag_total = True
        except:
            total_sum = 0.0



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
