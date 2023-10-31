import requests
from bs4 import BeautifulSoup


def login(username, password, login_url):
    session = requests.Session()
    login_data = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        return session
    else:
        raise Exception('Авторизация не удалась.')


def parse_data(session, target_url):
    response = session.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Ваш код для извлечения данных со страницы
    # ...
    title = soup.find('t976_menu-link').text.strip()
    return title


def main():
    username = 'lena.docha@gmail.com'
    password = 'cGZLY2xS'
    login_url = 'https://skilldesk.starta.university/members/login'
    target_url = 'https://skilldesk.starta.university/lessons'

    try:
        session = login(username, password, login_url)
        data = parse_data(session, target_url)
        print(data)
        print('Title:', data)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
