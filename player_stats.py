import json
from time import sleep
from selenium import webdriver
from parsel import Selector

# Create new Instance of Chrome
driver = webdriver.Chrome('/home/praveen/anaconda3/chromedriver')

# Go to desired website
driver.get('https://www.premierleague.com/players/1308/Gareth-Barry/overview')

# Wait 5 seconds for page to load
sleep(5)

# create Selector instance to scrape the content
sel = Selector(driver.page_source)

# Parse with Selector instance
pl_stats = sel.xpath('//*[@class="table"]')
players_apps = []

for pl_stat in pl_stats:
    # Scrape season
    season = pl_stat.xpath('.//*[@class="season"]//text()').extract_first()
    # Scrape player_club
    player_club = pl_stat.xpath('.//*[@class="team"]//text()').extract_first()
    # Scrape season_all_apps abd remove brackets and store into list    
    season_all_apps = pl_stat.xpath('.//*[@class="team"]/following-sibling::td/text()').extract_first().replace(')','').split('(')
    # first element in the list
    season_apps = int(season_all_apps[0])
    # second element in the list
    season_sub_apps = int(season_all_apps[1])
    # Scrape season_goals
    season_goals = int(pl_stat.xpath('.//*[@class="team"]/following-sibling::td/text()')[1].extract())      
    # Store details to player_app dictionary
    player_app = {'player_club': player_club, 'season': season, 'season_apps': season_apps, 'season_sub_apps': season_sub_apps, 'season_goals': season_goals}
    # append to outer dictionary players_app
    players_apps.append(player_app)

# To store the clubs the player played for 
all_clubs = []

# From the scraped data fetch the clubs name and append to all_clubs
for player in players_apps:
    all_clubs.append(player['player_club'])

# Delete the duplicate club names ie. dictionary keys can not be duplicated
all_clubs = list(dict.fromkeys(all_clubs))  

# To store the clubs and apperances for the player
club_app_goal = []

for club in all_clubs:
    # Total apperance for the club 
    total_app = sum(player['season_apps'] for player in players_apps if player['player_club'] == club)
    total_sub_app = sum(player['season_sub_apps'] for player in players_apps if player['player_club'] == club)
    total_goals = sum(player['season_goals'] for player in players_apps if player['player_club'] == club)
    # Club: Apperance store to list
    club_app_goal.append({'club' : club, 'total_app' : total_app, 'total_sub_app' : total_sub_app, 'total_goals' : total_goals})

# close the driver
driver.close()
