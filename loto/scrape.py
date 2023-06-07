
import dateutil.parser

import requests
from bs4 import BeautifulSoup
import csv

def scrape_eurojackpot_results(year):
    # send a GET request to the URL
    response = requests.get(f"https://www.euro-jackpot.net/en/results-archive-{year}")

    # parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # find the desired information using CSS selectors
    results = soup.select("table tbody tr")

    # extract the text from the elements
    rows = []
    for result in results:
        date_row = result.select_one("td:nth-of-type(1)").text.strip()
        date = dateutil.parser.parse(date_row)
        numbers = result.select("td:nth-of-type(2) span")
        all_numbers = [number.text.strip() for number in numbers]
        main_numbers = all_numbers[:5]
        main_numbers = [int(x) for x in main_numbers]
        add_numbers = all_numbers[-2:]
        add_numbers = [int(x) for x in add_numbers]
        rows.append([date, main_numbers, add_numbers])
        print(f"Date: {date}, Main numbers: {main_numbers}, add numbers: {add_numbers}")

    return rows


def main():
    # specify the range of years for which you want to scrape the results
    all_results = []
    for year in range(2023, 2011, -1):
        all_results.extend(scrape_eurojackpot_results(year))
    print(all_results)

    # write the results to a CSV file
    with open("eurojackpot_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "main_numbers", "add_numbers"])
        writer.writerows(all_results)


if __name__ == "__main__":
    main()

