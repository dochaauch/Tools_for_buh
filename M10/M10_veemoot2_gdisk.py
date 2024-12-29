import pandas as pd

# убираем ошибку
# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
# unable to get local issuer certificate (_ssl.c:1045)>
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def read_gsheet_to_pandas(sheet_name):
    # https://docs.google.com/spreadsheets/d/1vMQWNZTdzOqM-KOX-JefR5BOa1XbADgldYV0G6OeUnY/edit#gid=0
    file_id = "1vMQWNZTdzOqM-KOX-JefR5BOa1XbADgldYV0G6OeUnY"
    url = fr"https://docs.google.com/spreadsheets/d/{file_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url, header=0)
    #print(df.columns)
    #print(df.dtypes)
    return df


def create_first_row(lausendi_kuupaev):
    nr = lausendi_kuupaev.split('.')[2] + lausendi_kuupaev.split('.')[1]
    first_row = f'"{lausendi_kuupaev}", "{lausendi_kuupaev}","VL"' + '\r\n'
    return first_row, nr


def processing_df(df, lausendi_kuupaev, nr):
    #df['старые показания'] = pd.to_numeric(df['старые показания'], errors='coerce')
    # Replace commas with dots in all numeric columns
    df = df.apply(lambda x: x.str.replace(',', '.') if x.dtype == "object" else x)
    try:
        df['старые показания'] = df['старые показания'].str.replace('\xa0', "").astype(float)
    except:
        df['старые показания'] = df['старые показания'].astype(float)
    df['потребление'] = df['потребление'].astype(float)
    df['новые'] = df['новые'].astype(float)
    text_provodki = ""
    for index, row in df.iterrows():
        subkonto = row['номер']
        name = row['фамилия']
        aadress = row['адрес']
        vana = row['старые показания']
        uus = row['новые']
        m3 = row['потребление']
        text_provodki_row = \
            (f'"VL", "{lausendi_kuupaev}","VE","K1","VE","0",0.00,"VE:{nr}: {aadress} K1, {vana}-{uus}",'
                           f'"{subkonto}","1:3",{m3}')
        text_provodki += text_provodki_row + '\r\n'
    return text_provodki


def combine_text(first_row, text_provodki):
    return first_row + text_provodki


def write_to_txt(out, file_output):
    v = open(file_output, 'w')
    v.write(out)
    v.close()


def main():
    lausendi_kuupaev = '30.11.24'
    sheet_name = "NOV24"
    #file_output = '/Volumes/[C] Windows 10 (1)/Dropbox/_N/Metsa10_2011/veemotjad.txt'
    file_output = '/Users/docha/Library/CloudStorage/Dropbox/_N/Metsa10_2011/veemotjad.txt'
    df = read_gsheet_to_pandas(sheet_name)
    first_row, nr = create_first_row(lausendi_kuupaev)
    text_provodki = processing_df(df, lausendi_kuupaev, nr)
    out = combine_text(first_row, text_provodki)
    print(out)
    write_to_txt(out, file_output)


if __name__ == '__main__':
    main()



