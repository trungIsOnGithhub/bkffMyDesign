from helpers.main import *

def extract_data_from_source(**args):
    url = args[0]

    html_text = get_web_page_text(url)
    rows = parse_html(html_text)

    data = []

    for i in range(1, len(rows)):
        tds = rows[i].find_all('td')
        data.append({
            'rank': i,
            'stadium': clean_text(tds[0].text),
            'capacity': clean_text(tds[1].text).replace(',', '').replace('.', ''),
            'region': clean_text(tds[2].text),
            'country': clean_text(tds[3].text),
            'city': clean_text(tds[4].text),
            'thumb': 'https://' + tds[5].find('img').get('src').split("//")[1] if tds[5].find('img') else "NO_IMAGE",
            'home_team': clean_text(tds[6].text),
        })

    json = json.dumps(data)
    args.xcom_push(key='rows', value=json)

    return True

def transform_data_format():

def write_data_to_sink():


NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'