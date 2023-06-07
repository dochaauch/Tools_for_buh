import M10_scan_pdfplumber as M10
import re
import pprint
import os
import pdfplumber


def find_all_files(your_target_folder, r1):
    file_list = []
    for files_ in os.listdir(your_target_folder):
        if r1.search(files_):
            full_path = os.path.join(your_target_folder, files_)
            file_list.append(full_path)
            file_list.sort(key=str.lower)
    return file_list


def read_pdf_to_text_in_folder(pdf_files):
    text_dict = {}
    for ap in pdf_files:
        with pdfplumber.open(ap) as pdf:
            text = ""
            for page in pdf.pages:  # iterate over all pages in the PDF
                text += page.extract_text()
            key = os.path.basename(ap)
            text_dict[key] = text
    #print(text_dict)
    return text_dict


def findKwh_energia(input_string):
    # find all occurrences of the pattern
    pattern = r"Elekter\s+(\d+,\d+)\s+kWh"
    pattern1 = r"Elektriaktsiis.*, kogus (\d+,\d+) kWh"
    if re.findall(pattern, input_string):
        matches = re.findall(pattern, input_string)
    else:
        matches = re.findall(pattern1, input_string)
    matches = {float(match.replace(",", ".")) for match in matches}
    return round(sum(matches), 3)


def main():

    path = 'M10_in_arve_template.csv'
    r1 = re.compile(r'.*(elektrum|energia).*\.pdf$')  # вводим паттерн, который будем искать (все pdf)

    year_list = range(2013, 2024)

    for year in year_list:
        your_target_folder = f"/Users/docha/Google Диск/Metsa10/{year}"
        pdf_files = find_all_files(your_target_folder, r1)
        #print(pdf_files)
        template_dict = M10.read_csv_to_dict_template(path)
        # pprint.pprint(template_dict)
        arve_content = read_pdf_to_text_in_folder(pdf_files)
        kwt_dict = {}
        for file_name, text in arve_content.items():
            kwt_dict[file_name] = findKwh_energia(text)
        #print(kwt_dict)
        #pprint.pprint(arve_content)
        d, fd = M10.parse_invoice_data(arve_content, template_dict)
        #print(type(d), type(fd))
        #print(d)
        #print(fd)
        for firma, value in d.items():
            find_firma = d.get(firma)
            company = d.get(firma).firma
            uus_kokku = find_firma.total
            uus_arve = find_firma.arve_nr
            uus_date = find_firma.arve_kuup
            kWh = kwt_dict.get(firma)
            # try:
            #     kWh = findKwh_energia(d)
            # except:
            #     kWh = 0
            print(f"{company}; {uus_arve}; {uus_date}; {uus_kokku}; {kWh}")




if __name__ == '__main__':
    main()