import os

old_file = 'file.xstk'
new_file = 'file_new.xstk'

# Open the original file in binary mode
with open(old_file, 'rb') as f:
    # Read the entire file into memory as a binary string
    data = f.read()

# Replace the target string with the new string
data = data.replace(b'FromAddrStringraamatupidamine.rh@mail.ru', b'FromAddrStringraam@gmail.com')

# Write the modified data to a new file
with open(new_file, 'wb') as f:
    f.write(data)