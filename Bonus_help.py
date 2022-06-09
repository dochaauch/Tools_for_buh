import pickle
import os
import pprint

def save_dict_to_file(output):
    global system_text
    global list_of_files
    file_ = f'{your_target_folder}/{list_of_files[i_file]}'
    filename, file_extension = os.path.splitext(file_)
    dict_data = {}
    for line_ in output.splitlines():
        key, value = line_.split(': ')
        dict_data[key] = value
    file_date_ = os.stat(file_).st_birthtime
    file_date = datetime.datetime.fromtimestamp(file_date_).strftime('%y%m%d_%H%M')
    new_filename = f"{my_reverse_date(dict_data['kuupaev'])}_{dict_data['firma']}_{dict_data['arve nr']}_{file_date}"


def load_dict_from_file(file_name):
    with open(file_name, 'rb') as file_dict:
        output_dict = pickle.load(file_dict)
        return output_dict

your_target_folder = '/Volumes/[C] Windows 10 (1)/Users/docha/OneDrive/Leka/Tsekkid for test/Tsekkid aprill'
list_of_files = [fn for fn in os.listdir(your_target_folder)
                  if any(fn.endswith(ext) for ext in ['.pkl',])]
#pprint.pprint(list_of_files)

for file_ in list_of_files:
    dict_ = load_dict_from_file(f'{your_target_folder}/{file_}')
    for k, v in dict_.items():
        if k == 'kuupaev' or k == 'summa kokku':
            if ',' in v:
                print(file_, k, v)
