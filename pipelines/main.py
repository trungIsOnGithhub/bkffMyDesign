from datetime import datetime
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


def transform_data_format(**args):
    data = args['props'].xcom_pull(key='rows', task_ids='extract_data_from_source')

    data = json.loads(data)

    stadiums_df = pd.DataFrame(data)

    stadiums_df['location'] = stadiums_df.apply(lambda x: get_location_lat_long(x['country'], x['stadium']), axis=1)
    stadiums_df['thumb'] = stadiums_df['thumb'].apply(lambda x: x if x not in ['NO_IMAGE', '', None] else NO_IMAGE)
    stadiums_df['capacity'] = stadiums_df['capacity'].astype(int)

    # handle the duplicates
    duplicates = stadiums_df[stadiums_df.duplicated(['location'])]
    duplicates['location'] = duplicates.apply(lambda x: get_lat_long(x['country'], x['city']), axis=1)
    stadiums_df.update(duplicates)

    # push to xcom
    args['props'].xcom_push(key='rows', value=stadiums_df.to_json())

    return True


def write_data_to_sink():
    data = kwargs['props'].xcom_pull(key='rows', task_ids='transform_data_format')

    data = json.loads(data)
    data = pd.DataFrame(data)

    file_name = ('stadiums_cleaned_' + str(datetime.now().date())
                 + "_" + str(datetime.now().time()).replace(":", "_") + '.csv')

    # data.to_csv('data/' + file_name, index=False)
    data.to_csv('' + file_name,
                storage_options={
                    'account_key': ''
                }, index=False)


NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'