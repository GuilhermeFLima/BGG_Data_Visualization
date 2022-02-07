import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import re

pattern = r'(?:href=\"/boardgamemechanic.*?)>([\w /-]+?)<'
regex = re.compile(pattern)

url = "https://boardgamegeek.com/boardgame/31260/agricola/credits"
driver = webdriver.Firefox()
driver.get(url)
source_text = driver.page_source
print(regex.findall(source_text))
driver.quit()

url2 = "https://boardgamegeek.com/boardgame/342942/ark-nova/credits"
driver = webdriver.Firefox()
driver.get(url2)
source_text = driver.page_source
print(regex.findall(source_text))
driver.quit()


# second pattern to find the names of the mechanics:
#pattern2 = r'(?:\"name\"):\"([\w ]+)\"'
# pattern2 = r'<td>([\w ]+)<span id='
# regex2 = re.compile(pattern2)
# print(regex2.findall(mechanics))
# print(html.find("\"boardgamemechanic\""))
#print(html)
