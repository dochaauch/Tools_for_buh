import datetime
import os
import re
import PyPDF2
import pdfplumber

def str_to_float(value):
    return float(value.replace(',', '.')) if value else 0.0

def extract_pdf_files(target_folder, pattern=r'/\d{6}.*\.pdf$'):
    pdf_files = []
    for dirpath, _, filenames in os.walk(target_folder):
        for items in filenames:
            file_full_path = os.path.abspath(os.path.join(dirpath, items))
            if re.search(pattern, file_full_path.lower()):
                pdf_files.append(file_full_path)
    pdf_files.sort(key=str.lower)
    return pdf_files

def merge_pdfs(pdf_files, output_file='merged.pdf'):
    pdf_writer = PyPDF2.PdfFileWriter()
    for file in pdf_files:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)
    with open(output_file, 'wb') as f:
        pdf_writer.write(f)

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)
    return text

def clean_text(raw):
    special_char_map = {
        ord('ä'): 'a', ord('ü'): 'u', ord('ö'): 'o', ord('õ'): 'o',
        ord('ž'): 'z', ord('š'): 's',
        ord('Ä'): 'A', ord('Ü'): 'U', ord('Ö'): 'O', ord('Õ'): 'O',
        ord('Z'): 'Z', ord('Š'): 's', ord('’'): ''
    }
    cleaned = raw.translate(special_char_map)
    cleaned = re.sub(r'\n+\s*\n*', '\n', cleaned.strip())
    return cleaned.replace('\\n', '\n')

def process_text(lists):
    patterns = {
        'KLIENT': lambda x: x.split(':')[1].split(',')[0].strip().ljust(25),
        'ARVE': lambda x: re.search(r'\d+', x).group(0),
        'Summa KM-ta:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(9),
        'Kaibemaks 20%:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(7),
        'Käibemaks 20%:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(7),
        'Kaibemaks 22%:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(7),
        'Käibemaks 22%:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(7),
        'Kokku:': lambda x: re.search(r'\d+,\d+', x).group(0).rjust(9),
        'Kuupaev:': lambda x: (x.strip().replace(' ', '')[8:18], x.strip().replace(' ', '')[-13:-3])
    }

    data = {'klient': '', 'arve': '', 'summaKMta': '', 'kibemaks': '', 'kokku': '', 'kuupaev': '', 'maksepaev': ''}
    results = []
    totals = {'Skta': 0.00, 'Skm': 0.00, 'Skokk': 0.00}

    for line in lists:
        for key, func in patterns.items():
            if key in line:
                result = func(line)
                if key == 'Kuupaev:':
                    data['kuupaev'], data['maksepaev'] = result
                    try:
                        d1 = datetime.datetime.strptime(data['kuupaev'], '%d.%m.%Y')
                        d2 = datetime.datetime.strptime(data['maksepaev'], '%d.%m.%Y')
                        diff_date = str((d2 - d1).days)
                    except ValueError:
                        diff_date = ''

                    tt = f"{diff_date}\t{data['kuupaev']}\t{data['maksepaev']}\t{data['klient']}\t{data['arve']}\t{data['kokku']}\t{data['kibemaks']}\t{data['summaKMta']}"
                    results.append(tt)
                    totals['Skta'] += str_to_float(data['summaKMta'])
                    totals['Skm'] += str_to_float(data['kibemaks'])
                    totals['Skokk'] += str_to_float(data['kokku'])
                    data = {key: '' for key in data}  # Reset the dictionary for the next entry
                else:
                    data[key.split(' ')[0].lower()] = result
                break

    totals_row = f"\n{'':<3}\t{'':<10}\t{'':<10}\t{'':<20}\t{'':<6}\t\t{totals['Skokk']:.2f}\t{totals['Skm']:.2f}\t{totals['Skta']:.2f}"
    results.append(totals_row)
    return results

def write_to_file(results, filename='output.txt'):
    with open(filename, 'w') as f:
        header = f"D\t{'kuupaev':<10}\t{'maksepaev':<10}\t{'klient':<20}\t{'arve':<8}\t{'kokku':<9}\t{'kaibemaks':<7}\t{'KMta':<7}\n"
        f.write(header)
        print(header)
        for result in results:
            f.write(result + '\n')
            print(result)

def main():
    target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2024-06"
    pdf_files = extract_pdf_files(target_folder)
    merge_pdfs(pdf_files)
    raw_text = extract_text_from_pdf('merged.pdf')
    cleaned_text = clean_text(raw_text)
    lists = re.split(r'\n', cleaned_text)
    results = process_text(lists)
    write_to_file(results)

if __name__ == "__main__":
    main()
