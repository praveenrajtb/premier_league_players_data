import json
from time import sleep
from selenium import webdriver
from parsel import Selector

# Create new Instance of Chrome

driver = webdriver.Chrome('/home/praveen/anaconda3/chromedriver')
sleep(5)

# Go to desired website

driver.get('https://www.premierleague.com/players')

# Wait 5 seconds for page to load
sleep(10)

# create Selector instance to scrape the content
sel = Selector(driver.page_source)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(20)

player_rows = sel.xpath('//*[contains(@class, "dataContainer indexSection")]/tr')

players_data = []
players_apps = []
print(len(player_rows))

for player in player_rows:

	# scrape player url
	player_url = player.xpath('.//td/a/@href').extract_first()

	# player url fills with https://
	player_url = player_url.replace('//','https://')

	# scrape player name
	player_name = player.xpath('.//td/a/text()').extract_first()

	# scrape player position
	player_position = player.xpath('.//*[@class="hide-s"]/text()').extract_first()

	# scrape player country
	player_country = player.xpath('.//*[@class="playerCountry"]/text()').extract_first()

	# Store details to player_data dictionary
	player_data = {'player_name': player_name, 'player_position': player_position, 'player_country': player_country, 'player_url': player_url}

	# append to outer dictionary players_data
	players_data.append(player_data)

for player in players_data:
	print(player['player_url'])

	# Go to desired website
	driver.get(player['player_url'])
	sleep(7)

	# create Selector instance to scrape the content
	sel = Selector(driver.page_source)
	pl_stats = sel.xpath('//*[@class="table"]')

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

	# Update dictionary with new elements	
	player.update({'performance':player_app})

# Open json file as write mode and dumps data to json file
with open('players_file.json', 'w') as fp:
	json.dump(players_data, fp)

sleep(2)

# close he driver
driver.close()
