import requests
from bs4 import BeautifulSoup
from database import DBDriver


def _get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def parse_heroes():
    url = "https://dota2.ru/heroes/"
    result = list()
    dota_url = "https://dota2.ru/"
    soup = _get_html(url)
    div_inf = soup.find("div", class_="lines")
    heroes_inf = div_inf.find_all("a")
    for heroes in heroes_inf:
        name = heroes.get("data-tooltipe")
        icon = heroes.find("img", class_="img-m-hero").get("src")
        portrait_name = name.replace(" ", "_").lower()
        portrait = f"/img/heroes/{portrait_name}/portrait.jpg"
        result.append({"hero_name": name,
                       "hero_icon": dota_url + icon,
                       "hero_portrait": dota_url + portrait})
    DBDriver.add_heroes(result)
    return result


# def parse_items():
#     url = "https://dota2.ru/items/"
#     result = list()
#     dota_url = "https://dota2.ru/"
#     soup = _get_html(url)
#     div_inf = soup.find("div", id="list")
#     all_items = div_inf.find_all("a")
#     for item in all_items:
#         name = item.find("div", class_="title").text
#         icon = item.find("img").get("src")
#         result.append({"name": name,
#                        "icon": dota_url + icon})
#     DBDriver.add_item(result)
#     return result

parse_heroes()
