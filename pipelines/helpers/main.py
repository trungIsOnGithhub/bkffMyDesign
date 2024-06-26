import requests
import logging
from bs4 import BeautifulSoup
from geopy import Nominatim

def get_web_page_text(url):
    logging.info("Getting Web Page from: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.text

    except requests.RequestException as e:
        logging.error(f"ERROR OCCURED IN get_web_page_text(url)")


def clean_text(text):
    text = str(text).strip()
    text = text.replace('&nbsp', '')

    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    text.replace('\t', '')
    text.replace('\n', '')

    return text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find_all("table")[2]

    return table.find_all("tr")

def get_location_lat_long(country, city):
    geolocator = Nominatim(user_agent='geoapiExercises')
    location = geolocator.geocode(f'{city}, {country}')

    if location is not None:
        return location.latitude, location.longitude

    return None


if __name__== '__main__':
    # test if all functions run smoothly
    try:
        html_text = get_web_page_text('https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity')
        html_table_rows = parse_html(html_text)

        for row in html_table_rows:
            tds = row.find_all('td')

            for td in tds:
                print(td)

            print('---------------')
    except Exception as e:
        logging.error(e)