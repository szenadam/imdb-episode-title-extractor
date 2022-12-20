import sys
import datetime
import json
import logging
import argparse
import requests

from bs4 import BeautifulSoup


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s', datefmt="%Y-%m-%d %I:%M:%S")

    args = parse_arguments()
    name = args.name
    series_id = args.id
    num_of_seasons = int(args.seasons) + 1
    should_sanitize = args.sanitize

    result = extract_data(name, series_id, num_of_seasons, should_sanitize)
    write_to_file(name, series_id, result)
    return 0


def parse_arguments():
    """ Parse input arguments. """
    parser = argparse.ArgumentParser(prog="EpisodeTitleExtractor",
                                     description="Extract episode titles for a series from IMDB.")
    parser.add_argument("-n", "--name", required=True, help="Name of the series.")
    parser.add_argument("-i", "--id", required=True, help="ID used in IMDB for the series. Get it from URL.")
    parser.add_argument("-s", "--seasons", required=True, type=int, help="Number of seasons for the series.")
    parser.add_argument("--sanitize", action="store_true",
                        help="Sanitize title. Remove spaces and non ASCII characters.")
    args = parser.parse_args()
    return args


def extract_data(title, series_id, num_of_seasons, should_sanitize):
    """ Loop through every season of the series and extract season/episode number and title. """
    episodes_list = list()
    total = 0
    for i in range(1, num_of_seasons):
        logging.info(f'Getting season {i} of {title}')
        url = f"https://www.imdb.com/title/{series_id}/episodes?season={i}"
        resp = requests.get(url)

        if resp.status_code == 404:
            logging.error("Series not found")
            sys.exit(-1)

        soup = BeautifulSoup(resp.text, "html.parser")

        episodes = get_episodes(soup)
        titles = get_titles(soup, should_sanitize)

        if len(episodes) != len(titles):
            logging.error("Length mismatch")
            sys.exit(-1)
        total += len(episodes)
        season = dict(zip(episodes, titles))
        episodes_list.append(season)
    result = dict()
    result["title"] = title
    result["total"] = total
    result["episodes"] = episodes_list
    return result


def write_to_file(title, series_id, result):
    """ Write extracted data to json file. """
    logging.info(json.dumps(result, indent=2))
    out_file_name = f"./out/{title}-{series_id}-episodes-{datetime.date.today()}.json"
    with open(out_file_name, "w", encoding='utf-8') as f:
        f.write(json.dumps(result, indent=2))


def get_episodes(soup):
    """ Get episode numbers text from page and return them in a list. """
    ep_numbers = soup.select("div.list_item div.image div.hover-over-image div")
    keys = list()
    for e in ep_numbers:
        keys.append(e.get_text().replace(", ", ""))
    return keys


def get_titles(soup, should_sanitize):
    """ Get episode titles from page and return them in a list. """
    titles = soup.select("div.list_item div.info strong")
    values = list()
    for title in titles:
        title_text = title.get_text()
        if (should_sanitize):
            title_text = sanitize_title(title_text)
        values.append(title_text)
    return values


def sanitize_title(title):
    result = title
    replacement_pairs = [
        (" ", "_"),
        (",", ""),
        ("'", ""),
        ("#", ""),
        ("?", ""),
        ("!", ""),
        ("&", "and"),
        (".", ""),
        ("(", ""),
        (")", ""),
        ("[", ""),
        ("]", ""),
    ]
    for i in replacement_pairs:
        result = result.replace(i[0], i[1])
    return result


if __name__ == "__main__":
    main()
