#import required libaries
from selenium import webdriver #selenium is used to automate browser --> prevents bot detection
from selenium.webdriver.chrome.service import Service #allows to give path to chromedriver
from bs4 import BeautifulSoup #beautifulsoup used to extract html from page
import pandas as pd #used to create dataframe and save it in a csv file
import time

players = {} #dictionary to store players --> will convert to list later as dicitonaries dont allow duplicates --> going to use name of player as key and values will be all other attributes
#this is only take the stats of a player's latest team as the table has 3 tables if a player gets traded mid season --> combined stats, old team and new team

#download chrome driver and replace path
service = Service(r"C:\Users\udula\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe") #using Service to tell selenium where chromdriver.exe is located

driver = webdriver.Chrome(service=service)
url = "https://www.basketball-reference.com/leagues/NBA_2025_per_game.html"
driver.get(url)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser") #BeautifulSoup converts html into parsable tree - .page_source gets all of the html from the page
driver.quit() #close chrome browser

table = soup.find("table", id="per_game_stats") #gets table
rows = table.tbody.find_all("tr") #finds the rows (1 row = 1 player)

for row in rows: #skip header rows inside table
    if row.get("class") == ["thead"]:
        continue

    #get stats of players
    name = row.find("td", {"data-stat": "name_display"}).text
    pos = row.find("td", {"data-stat": "pos"}).text
    team = row.find("td", {"data-stat": "team_name_abbr"}).text
    pts = row.find("td", {"data-stat": "pts_per_g"}).text
    ast = row.find("td", {"data-stat": "ast_per_g"}).text
    trb = row.find("td", {"data-stat": "trb_per_g"}).text
    stl = row.find("td", {"data-stat": "stl_per_g"}).text
    blk = row.find("td", {"data-stat": "blk_per_g"}).text

    #put each stat into dictionary --> key is player name
    players[name]=([name, pos, team, pts, ast, trb, stl, blk])


players_list = list(players.values()) #convert dictionary of players to list

#PANDAS

df = pd.DataFrame(players_list, columns=["Name", "Position", "Team", "Ppg", "Ast", "Trb", "Stls", "Blks"]) #put data in list to dataframe via pandas
df.to_csv("nba_stats.csv", index=False)
    



