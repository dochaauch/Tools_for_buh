import os

folder_path = '/Volumes/[C] Windows 10 (1)/Users/docha/OneDrive/Leka/TSEKKID/UNION tsekkid/Union Tsekkid 04y.2023'

for filename in os.listdir(folder_path):
    if filename.startswith('.'):
        print(filename)

answer = input("do you want to delete them? y/n ")
for filename in os.listdir(folder_path):
    if answer == 'y':
        if filename.startswith('.'):
            os.remove(os.path.join(folder_path, filename))
            print(f"file {filename} is deleted")