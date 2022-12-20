# Series Episode-Title Extractor from IMDB

Quickly extract a list of key-value pairs of episodes and titles.

## Requirements

- Python3
    - BeautifulSoup4

## Usage

```sh
python main.py [-h] -n NAME -i ID -s SEASONS [--sanitize]

Extract episode titles for a series from IMDB.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the series.
  -i ID, --id ID        ID used in IMDB for the series. Get it from URL.
  -s SEASONS, --seasons SEASONS
                        Number of seasons for the series.
  --sanitize            Sanitize title. Remove spaces and non ASCII characters.
```