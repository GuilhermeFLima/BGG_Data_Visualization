import pandas as pd
import requests
from selenium import webdriver
import re

# script to create a Pandas DataFrame with game id and the url address
# of  the game's main page at bgg

def geturl(game_id: str) -> str:
    """
    Returns the url for bgg main page of game, given id.
    :param gameid: string with the number id for game.
    :return: bgg url string.
    """
    main_page_url = "https://boardgamegeek.com/boardgame/" + game_id
    main_page = requests.get(main_page_url)
    main_page_text = main_page.text
    address_pattern = '(https://boardgamegeek.com/boardgame/[\d]+/[\w-]+)'
    address_regex = re.compile(address_pattern)
    address_find = address_regex.search(main_page_text)
    main_address = main_page_text[address_find.start():address_find.end()]
    return main_address
