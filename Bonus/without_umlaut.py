def translateString(our_string):
    special_char_map = {ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
                        ord('ž'): 'z', ord('š'): 's',
                        ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
                        ord('Z'): 'Z', ord('Š'): 'S', ord('’'): '',
                        ord('Ł'): 'L', ord('Ę'): 'E',
                        }
    return our_string.translate(special_char_map)