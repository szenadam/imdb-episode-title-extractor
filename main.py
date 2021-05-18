import sys
import requests
import json

from bs4 import BeautifulSoup


def main():
    series_id = 'foobar'
    num_of_seasons = 16 + 1

    result = list()

    for i in range(1, num_of_seasons):
        url = f"https://www.imdb.com/title/{series_id}/episodes?season={i}"
        resp = requests.get(url)

        if resp.status_code == 404:
            print("Series not found")
            sys.exit(-1)

        soup = BeautifulSoup(resp.text, "html.parser")

        episodes = get_episodes(soup)
        titles = get_titles(soup)

        if len(episodes) != len(titles):
            print("Length mismatch")
            sys.exit(-1)

        season = dict(zip(episodes, titles))
        result.append(season)

    print(json.dumps(result, indent=2))
    return 0


def get_episodes(soup):
    """ Get episode numbers text from page and return them in a list. """
    ep_numbers = soup.select("div.list_item div.image div.hover-over-image div")
    keys = list()
    for e in ep_numbers:
        keys.append(e.get_text())
    return keys


def get_titles(soup):
    """ Get episode titles from page and return them in a list. """
    titles = soup.select("div.list_item div.info strong")
    values = list()
    for t in titles:
        values.append(t.get_text())
    return values

def normalize_keys():
    """ Replace spaces and special characters in dict keys. """
    pass

def normalize_values():
    """ Replace spaces and special characters in dict values. """
    pass


if __name__ == "__main__":
    main()
