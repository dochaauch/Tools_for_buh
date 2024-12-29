import datetime
import os
import re
import pdfplumber


def str_to_float(s):
    """Convert string to float, replacing comma with dot."""
    return float(s.replace(',', '.'))


def find_pdf_files(folder):
    """Find PDF files in the given folder matching the pattern."""
    pdf_files = []
    pattern = re.compile(r'/\d{6}.*\.pdf$')
    for dirpath, _, filenames in os.walk(folder):
        for item in filenames:
            file_path = os.path.abspath(os.path.join(dirpath, item))
            if pattern.search(file_path.lower()):
                pdf_files.append(file_path)
    return sorted(pdf_files, key=str.lower)


def merge_pdf_files(pdf_files, output_file='merged.pdf'):
    """Merge multiple PDF files into one."""
    pdf_merger = pdfplumber.PDF()
    for file_path in pdf_files:
        with pdfplumber.open(file_path) as pdf:
            pdf_merger.extend(pdf.pages)

    pdf_merger.save(output_file)


def extract_text_from_pdf(file_path):
    """Extract text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    special_char_map = {
        'ä': 'a', 'ü': 'u', 'ö': 'o', 'õ': 'o',
        'ž': 'z', 'š': 's',
        'Ä': 'A', 'Ü': 'U', 'Ö': 'O', 'Õ': 'O',
        'Z': 'Z', 'Š': 's', "'": '',
    }
    for char, replacement in special_char_map.items():
        text = text.replace(char, replacement)

    return re.sub(r'\n+\s*\n*', '\n', text.strip())

def parse_invoice_data(text):
    """Parse invoice data from text."""
    lines = text.split('\n')
    data = {
        'klient': '', 'arve': '', 'summa_km_ta': 0.0,
        'kaibemaks': 0.0, 'kokku': 0.0, 'kuupaev': '', 'maksepaev': ''
    }

    parse_actions = {
        'KLIENT': lambda line: setattr(data, 'klient', parse_client_name(line)),
        'ARVE': lambda line: setattr(data, 'arve', re.search(r'(\d+)', line).group(1)),
        'Summa KM-ta:': lambda line: setattr(data, 'summa_km_ta', str_to_float(re.search(r'(\d+,\d+)', line).group(1))),
        'Kokku:': lambda line: setattr(data, 'kokku', str_to_float(re.search(r'(\d+,\d+)', line).group(1))),
        'Kuupaev:': lambda line: parse_dates(line, data),
    }

    tax_keywords = ['Kaibemaks 20%:', 'Käibemaks 20%:', 'Käibemaks 22%:', 'Kaibemaks 22%:']

    for line in lines:
        for keyword, action in parse_actions.items():
            if keyword in line:
                action(line)
                break
        else:
            if any(tax in line for tax in tax_keywords):
                data['kaibemaks'] = str_to_float(re.search(r'(\d+,\d+)', line).group(1))

    return data

def parse_client_name(line):
    """Parse client name from the line."""
    klient = line.split(':')[1]
    if 'OU,' in klient or 'AS,' in klient or re.search(r'^KLIENT:\s((OU|AS)\s.*)', line):
        klient = klient.split(',')[0]
    elif re.search(r'\s{2,}', line):
        klient = re.split(r'\s{2,}', re.search(r'KLIENT: (.*)', line).group(1))[0]
    elif re.search(r'^.*(OU|AS)', line):
        klient = re.search(r'^KLIENT: (.*(OU|AS))', line).group(1)
    return klient.strip()[:24].ljust(25)

def parse_dates(line, data):
    """Parse invoice and due dates from the line."""
    dates = line.strip().replace(' ', '')
    data['kuupaev'] = dates[8:18]
    data['maksepaev'] = dates[-13:-3]

def calculate_date_diff(date1, date2):
    """Calculate difference between two dates."""
    try:
        d1 = datetime.datetime.strptime(date1, '%d.%m.%Y')
        d2 = datetime.datetime.strptime(date2, '%d.%m.%Y')
        return str(d2 - d1).split(',')[0].split(' ')[0]
    except ValueError:
        return ''

def process_invoices(folder):
    """Process invoices from the given folder."""
    pdf_files = find_pdf_files(folder)
    merge_pdf_files(pdf_files)

    text = extract_text_from_pdf('merged.pdf')

    totals = {'summa_km_ta': 0.0, 'kaibemaks': 0.0, 'kokku': 0.0}

    with open('output.txt', 'w') as f:
        header = ('D\tkuupaev\tmaksepaev\tklient\tarve\tkokku\tkaibemaks\tKMta\n')
        f.write(header)
        print(header)

        invoice_data = parse_invoice_data(text)
        diff_date = calculate_date_diff(invoice_data['kuupaev'], invoice_data['maksepaev'])

        row = (f"{diff_date}\t{invoice_data['kuupaev']}\t{invoice_data['maksepaev']}\t"
               f"{invoice_data['klient']}\t{invoice_data['arve']}\t"
               f"{invoice_data['kokku']:9.2f}\t{invoice_data['kaibemaks']:7.2f}\t"
               f"{invoice_data['summa_km_ta']:9.2f}\n")

        f.write(row)
        print(row)

        for key in totals:
            totals[key] += invoice_data[key]

        totals_row = (f"\n\t\t\t\t\t{totals['kokku']:9.2f}\t"
                      f"{totals['kaibemaks']:7.2f}\t{totals['summa_km_ta']:9.2f}\n")
        f.write(totals_row)
        print(totals_row)

if __name__ == "__main__":
    target_folder = "/Users/docha/Library/CloudStorage/GoogleDrive-mob37256213753@gmail.com/Мой диск/Bonus/2024-06"
    process_invoices(target_folder)