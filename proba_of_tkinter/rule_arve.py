re_arve_list = [
    r'(?:Saateleht|Arve|TSEKK|kviitung|Tšekk)'
    r'(?! summa)\s?[-\/\\\s]?\s?(?:arve|saateleht)?\s?(?:nr|number)?\.?:?\s?#?(.*)',
    #r'Arve-Saateleht nr.:\s(.*)',
    #r'Arve nr\.\s(.*)',
    #r'ARVE NR\s(.*)',
    #r'Arve\s*(.*)',

    #r'Kviitung:\s(.*)',

    #r'Saateleht-arve nr. (.*)',
    #r'SAATELEHT\s(.*)',

    #r'Sularahaarve nr.\s(.*)',
    #r'TSEKK/ARVE\s(.*)',

    r'(?:invoice)\s?(?:nr)?\.?:?\s?(.*)',

    r'(?:Izdruka|ceks|čeks|Dokuments|DOK|Rēķins|Kvits)\b\.?\s?(?:nr)?\.?:?\s?#?(.*)',
    #r'Ceks (.*)',
    #r'čeks (.*)',
    

    ]


'''
Arve-Saateleht nr. 1460
Arve-saateleht nr.: 4453
Arve-Saateleht nr.: 02223-45
Arve-Saateleht nr 1460
Arve-Saateleht 5555
Arve 6666
Saateleht 6
ARVE NR 7-9945 ex
Arve nr. 775
Saateleht-arve nr. 77
SAATELEHT rr
Sularahaarve nr.55
Sularahaarve nr. 55
Sularahaarve nr 55
Kviitung nr.443-55g
Kviitung ffe
TSEKK/ARVE nr556
DOK. #00009568

'''
