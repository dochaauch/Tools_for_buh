from trello import TrelloClient
import confidence
import re

api_key = confidence.api_key
api_token = confidence.api_token

client = TrelloClient(api_key=api_key, api_secret=api_token)

board_id = confidence.board_id

board = client.get_board(board_id)

lists = board.list_lists()

def find_links_with_word(card_part, word):
    urls = set()
    pattern = rf"(?P<url>https?://.* ?{word}/\d+)"
    match = re.search(pattern, card_part)
    if match:
        url = match.group("url")
        print(f"   - Ссылка {word}: {url}")
        urls.add(url)
    return urls

for trello_list in lists:
    if trello_list.name != "Done":
        print(f"Список: {trello_list.name}")
        cards = trello_list.list_cards()
        for card in cards:
            print(f" - {card.name}")

            # Извлечение ссылки из описания
            # if "http" in card.description:
            #     pattern = r"\[(?P<url>https?://[^\]]+)\]"
            #     match = re.search(pattern, card.description)
            #     if match:
            #         issue_url = match.group("url")
            #         print(f"   - Ссылка на issue (из описания): {issue_url}")
            if "http" in card.description:
                print("***descr")
                print(card.description)
                issue_url = find_links_with_word(card.description, "issue")
                pull_url = find_links_with_word(card.description, "pull")


            # Извлечение ссылки из вложений
            for attachment in card.attachments:
                if "http" in attachment['url']:
                    print('***attach')
                    print(attachment['url'])
                    issue_url = find_links_with_word(attachment['url'], "issue")
                    pull_url = find_links_with_word(attachment['url'], "pull")

            # Извлечение ссылки из комментариев
            for comment in card.get_comments():
                #print(comment)
                if "http" in comment['data']['text']:
                    print('***comm')
                    print(comment['data']['text'])
                    issue_url = find_links_with_word(comment['data']['text'], "issue")
                    pull_url = find_links_with_word(comment['data']['text'], "pull")







