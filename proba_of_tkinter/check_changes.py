import pickle
import os
from collections import Counter
import datetime

from icecream import ic

#your_target_folder = '/Users/docha/Documents/Tsekk_check'
your_target_folder = '/Volumes/[C] Windows 10 (1)/Users/docha/OneDrive/Leka/Tsekkid for test/tsekkid Juuli 2022'


def time_format():
    return f'{datetime.datetime.now()}|> '
ic.configureOutput(prefix=time_format, includeContext=True)


def find_uniq_names(your_target_folder):
    #создаем список всех файлов в папке, без расширения.
    #не удаляем дубли! нужно количество файлов
    uniq_names = list()
    for file_ in find_all_files(your_target_folder):
        filename, file_extension = os.path.splitext(file_)
        uniq_names.append(filename)
    return uniq_names


def count_file_with_uniq(your_target_folder, extension='', count_=1):
    uniq_names = find_uniq_names(your_target_folder)

    dict_count = Counter(uniq_names)
    #считаем количество файлов
    i = 0
    list_not_full = list()
    for filename, file_count in dict_count.items():
        if file_count < 3:
            filter_ext = filter(lambda a: filename in a, find_all_files(your_target_folder, extension))
            f_ = list(filter_ext)
            ic(f_)
            if len(f_) == count_:
                f_ = f_[0]
                i += 1
                print(i, f_)
                list_not_full.append((i, f_))
    ic(list_not_full)
    return list_not_full


def del_ocr_without_jpg(your_target_folder):
    # удаление файлы, которые есть только один раз в папке

    ic(count_file_with_uniq(your_target_folder))
    for _, file_ in count_file_with_uniq(your_target_folder):
        filename, file_extension = os.path.splitext(file_)
        if file_extension != 'jpg':
            print('удаляем следующие файлы, у которых нет jpg', file_)
            #os.remove(file_)



def load_dict_from_file(file_name):
    with open(file_name, 'rb') as file_dict:
        return pickle.load(file_dict)


def find_all_files(your_target_folder, exten=''):
    full_list = []
    for dirpath, _, filenames in os.walk(your_target_folder):
        for items in filenames:
            file_full_path = os.path.abspath(os.path.join(dirpath, items))
            if exten == '':
                full_list.append(file_full_path)
            if file_full_path.endswith(f'.{exten}'):
                full_list.append(file_full_path)
    full_list.sort(key=str.lower)
    return full_list


def proc_(l, count_):
    return f'{round((l - count_) / l * 100, 2)}%'

print('удаляем файлы')
del_ocr_without_jpg(your_target_folder)


count_not_changed = 0
count_ch_sum = 0
count_ch_kuupaev = 0
count_ch_firma = 0
count_ch_arve = 0
for file_ in find_all_files(your_target_folder, 'pkl'):
    ind_ = find_all_files(your_target_folder, 'pkl').index(file_)
    d1 = load_dict_from_file(file_)
    if d1['not_changed'] == 'no':
        count_not_changed += 1
    if d1['change_log']:
        ic(ind_, file_, d1['change_log'])
        if 'summa' in d1['change_log'] or 'km' in d1['change_log'] or 'summa kokku' in d1['change_log']:
            count_ch_sum += 1
        if 'arve nr' in d1['change_log']:
            count_ch_arve += 1
        if 'kuupaev' in d1['change_log']:
            count_ch_kuupaev += 1
        if 'firma' in d1['change_log']:
            count_ch_firma += 1



l = len(find_all_files(your_target_folder, 'pkl'))

print('всего обработанных файлов', l)
print('исправленные файлы', count_not_changed)
print('изначально корректные файлы', l - count_not_changed)

proc = proc_(l, count_not_changed)
proc_sum = proc_(l, count_ch_sum)
proc_kuupaev = proc_(l, count_ch_kuupaev)
proc_firma = proc_(l, count_ch_firma)
proc_arve = proc_(l, count_ch_arve)

print('процент корректно прочитанных файлов', proc)
print('***')
print('исправленные суммы', count_ch_sum, proc_sum)
print('исправление даты', count_ch_kuupaev, proc_kuupaev)
print('исправленные фирмы', count_ch_firma, proc_firma)
print('исправленные номера счета', count_ch_arve, proc_arve)

count_file_with_uniq(your_target_folder, count_=2)
















