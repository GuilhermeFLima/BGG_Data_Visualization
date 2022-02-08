import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from selenium import webdriver
import re


# The main page of each board game can be accessed via "https://boardgamegeek.com/boardgame/" + game_id ,
# without mentioning its "web name", ie: "https://boardgamegeek.com/boardgame/135779"
# redirects to
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"

# The list of mechanisms if found on the "credits" page (in javascript code), and not the main page.
# The credits page needs the "web name" of the boardgame, eg:
# "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york/credits"

# We need to get the actual page address since the name of the boardgame and
# the name on the webpage (ie the "web name") can be different:
# eg: "A Fake Artist Goes to New York" and "https://boardgamegeek.com/boardgame/135779/fake-artist-goes-new-york"


# first we get the address
game_id = "271055"
main_page_url = "https://boardgamegeek.com/boardgame/" + game_id
main_page = requests.get(main_page_url)
main_page_text = main_page.text
address_pattern = '(https://boardgamegeek.com/boardgame/[\d]+/[\w-]+)'
address_regex = re.compile(address_pattern)
address_find = address_regex.search(main_page_text)
main_address = main_page_text[address_find.start():address_find.end()]

# now we grab the list of mechanisms
pattern = r'(?:href=\"/boardgamemechanic.*?)>([,:\w /-]+?)<'
regex = re.compile(pattern)
url = main_address + "/credits"
driver = webdriver.Firefox()
driver.get(url)
source_text = driver.page_source
print(regex.findall(source_text))
driver.quit()

