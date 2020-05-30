import requests
from main_parser import HEADERS


def get_page_api(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_statistics_data(page_api):
    statistics_list = list()
    players = page_api['players']
    for player in players:
        kills = player['kills']
        deaths = player['deaths']
        assists = player['assists']

        last_hits = player['last_hits']
        denies = player['denies']

        gold_per_min = player['gold_per_min']
        xp_per_min = player['xp_per_min']

        damage = player['hero_damage']
        tower_damage = player['tower_damage']

        statistics_list.append({
            'kills': kills,
            'deaths': deaths,
            'assists': assists,
            'last_hits': last_hits,
            'denies': denies,
            'gold_per_min': gold_per_min,
            'xp_per_min': xp_per_min,
            'damage': damage,
            'tower_damage': tower_damage})

    print(statistics_list)


def main():
    match_id = '5442927048'
    url_api = 'https://api.opendota.com/api/matches/' + match_id

    response = get_page_api(url_api)

    if response.status_code == 200:
        get_statistics_data(response.json())
    else:
        print('Error')


if __name__ == '__main__':
    main()