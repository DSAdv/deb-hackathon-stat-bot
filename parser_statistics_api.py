import requests
from main_parser import HEADERS


class Statistics:
    def __init__(self, match_id):
        self.match_id = match_id

    def get_page_api(self):
        r = requests.get(
            f'https://api.opendota.com/api/matches/{self.match_id}',
            headers=HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            print('Error')

    def get_statistics_data(self):
        statistics_list = list()
        page_api = self.get_page_api()
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

        return statistics_list