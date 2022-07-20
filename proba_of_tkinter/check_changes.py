import pickle
import os

your_target_folder = '/Users/docha/Documents/Tsekk_check'
count_ = 0

def load_dict_from_file(file_name):
    with open(file_name, 'rb') as file_dict:
        output_dict = pickle.load(file_dict)
        return output_dict


def find_all_files(your_target_folder):
    full_list = []
    for dirpath, _, filenames in os.walk(your_target_folder):
        for items in filenames:
            file_full_path = os.path.abspath(os.path.join(dirpath, items))
            if file_full_path.endswith('.pkl'):
                full_list.append(file_full_path)
            else:
                pass
    full_list.sort(key=str.lower)
    return full_list


for file_ in find_all_files(your_target_folder):
    d1 = load_dict_from_file(file_)
    if d1['not_changed'] == 'no':
        count_ += 1

l = len(find_all_files(your_target_folder))
print('всего обработанных файлов', l)
print('исправленные файлы', count_)
print('изначально корректные файлы', l - count_)

proc = (l - count_) / l * 100
print('процент корректно прочитанных файлов', proc)


