import requests
from bs4 import BeautifulSoup


# Функция для получения данных из блока
def extract_data(block):
    title = block.find('div', class_='t778__title').text.strip()
    date = block.find('p', text='Date:').next_sibling.strip()
    subject = block.find('p', text='Subject:').next_sibling.strip()
    teacher = block.find('p', text='Teacher:').next_sibling.strip()
    keywords = block.find('p', text='Key words:').next_sibling.strip()
    group = block.find('p', text='Group:').next_sibling.strip()
    link = block.find('a', text='View lesson')['href']
    return [title, date, subject, teacher, keywords, group, link]


# URL страницы для парсинга
url = 'https://skilldesk.starta.university/lessons'

# Список для хранения данных
data = []

# Парсинг страницы
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлечение блоков с данными
    blocks = soup.find_all('div', class_='t778__content')
    for block in blocks:
        extracted_data = extract_data(block)
        data.append(extracted_data)

    # Проверка наличия кнопки "Загрузить ещё"
    show_more_button = soup.find('div', class_='t778__showmore')
    if show_more_button is None:
        break

    # Обновление URL для загрузки следующей страницы
    load_more_url = show_more_button.find('a')['href']
    url = f"https://skilldesk.starta.university/lessons{load_more_url}"

# Вывод данных
for row in data:
    print(row)