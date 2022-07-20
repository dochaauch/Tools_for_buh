#8 цифр для эстонского номера, 11 цифр для латышского
re_reg_nr_list = [r'Reg.kood\s(\b\d{8,11}\b)',
                      r'Reg.\s*nr\.*:*\s*(\b\d{8,11}\b)',
                      r'Reg:(\d{8,11})',
                      r'REG.NR.:\s*(\d{8,11})',
                      r'Registrikood:\s*(\d{8,11})'
                      ]