import requests
from bs4 import BeautifulSoup
from database import DBDriver

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': '*/*'}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    sections = soup.find('div', class_='col-xs-30').find_all('section')
    return sections


def get_tournament_matches(sections):
    list_matches = list()
    for section in sections:
        league = section.find('header').find('small').get_text()
        if league == 'Професійна':
            tournament_name = section.find('header').find('img').get('alt')
            href_tournament = section.find('header').find('a').get('href')
            reference_tournamet = 'https://uk.dotabuff.com' + href_tournament
            matches = section.find('div', class_='row scores').find_all('a')
            for match in matches:
                match_href_id = match.get('href').replace('/', ' ').split()
                match_id = int(match_href_id[1])

                teams = match.find_all('div', class_='name')
                team_one = teams[0].find('span', class_='team-text').get_text()
                team_two = teams[1].find('span', class_='team-text').get_text()

                killings = match.find('div', class_='match-score-info').find_all('span')
                team_one_killing = killings[0].get_text()
                team_two_killing = killings[2].get_text()

                divs_heroes_team_one = match.find('div', class_='match-score-heroes').find('div', class_='radiant').find_all('div')
                list_heroes_team_one = list()
                for div in divs_heroes_team_one:
                    list_heroes_team_one.append(div.find('img').get('alt'))
                heroes_team_one = list_heroes_team_one[0] + ', ' + list_heroes_team_one[1] + ', '\
                                  + list_heroes_team_one[2] + ', ' + list_heroes_team_one[3] + ', ' \
                                  + list_heroes_team_one[4]


                divs_heroes_team_two = match.find('div', class_='match-score-heroes').find('div', class_='dire').find_all('div')
                list_heroes_team_two = list()
                for div in divs_heroes_team_two:
                    list_heroes_team_two.append(div.find('img').get('alt'))
                heroes_team_two = list_heroes_team_two[0] + ', ' + list_heroes_team_two[1] + ', ' \
                                  + list_heroes_team_two[2] + ', ' + list_heroes_team_two[3] + ', ' \
                                  + list_heroes_team_two[4]

                game_time = match.find('div', class_='match-score-info').find('div', class_='pull-left').get_text()
                datetime = match.find('div', class_='match-score-info').find('div',
                        class_='pull-right').find('time').get('title').split()
                time = datetime[-2]

                list_matches.append({
                    'tournament': tournament_name,
                    'team1': team_one,
                    'team2': team_two,
                    'number_of_murders_t1': int(team_one_killing),
                    'number_of_murders_t2': int(team_two_killing),
                    'game_end_time': time,
                    'list_heroes1': heroes_team_one,
                    'list_heroes2': heroes_team_two,
                    'match_id': match_id,
                    'match_url': reference_tournamet,
                    'game_time': game_time
                })

        else:
            continue
        DBDriver.add_match(list_matches)
    return list_matches


def watching_matches(content):
    print(get_tournament_matches(content))


def main():
    url = 'https://uk.dotabuff.com/esports/scores'
    html = get_html(url)

    if html.status_code == 200:
        watching_matches(get_content(html.text))
    else:
        print('Error')


if __name__ == '__main__':
    main()