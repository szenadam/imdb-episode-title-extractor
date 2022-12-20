import sys
import datetime
import json
import logging
import argparse
import requests

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-i", "--id", required=True)
    parser.add_argument("-s", "--seasons", required=True, type=int)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    title = args.name
    series_id = args.id
    num_of_seasons = int(args.seasons) + 1

    episodes_list = list()

    for i in range(1, num_of_seasons):
        logging.info(f'Getting season {i} of {title}')
        url = f"https://www.imdb.com/title/{series_id}/episodes?season={i}"
        resp = requests.get(url)

        if resp.status_code == 404:
            logging.error("Series not found")
            sys.exit(-1)

        soup = BeautifulSoup(resp.text, "html.parser")

        episodes = get_episodes(soup)
        titles = get_titles(soup)

        if len(episodes) != len(titles):
            logging.error("Length mismatch")
            sys.exit(-1)

        season = dict(zip(episodes, titles))
        episodes_list.append(season)
    result = dict()
    result["title"] = title
    result["episodes"] = episodes_list

    logging.info(json.dumps(result, indent=2))
    with open(f'{series_id}.json', "w", encoding='utf-8') as f:
        f.write(json.dumps(result, indent=2))
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
