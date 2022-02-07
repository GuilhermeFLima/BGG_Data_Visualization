import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://boardgamegeek.com/boardgame/31260/agricola"
page = urlopen(url)
html = page.read().decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")

print(html.find("\"boardgamemechanic\""))
print(html.find("boardgamemechanic"))