import pygame as pg
import requests
import sys 

'''
The loading screen uses a simple API in order to show Dad jokes on the loading screen of the game. 
'''

def start_loading_screen():
	# Pygame essentials 
	pg.font.init() 
	screen = pg.display.set_mode((1200, 720))
	clock = pg.time.Clock() 
	font = pg.font.Font("assets/font.ttf", 17)

	# API 
	response = requests.get("https://icanhazdadjoke.com/slack")
	answer = response.json()

	# Colour constants 
	BACKGROUND_COLOR = '#0d0e2e'
	LIGHT_GRAY = '#ff3300' 
	GRAY = '#33cc33'
 
	# Button variables.
	button_rect = pg.Rect(120, 600, 1000, 80)
	max_width = 1000  # Maximum width of the rect.
	max_time = 3  # Time after which the button should be filled.
	# Coefficient to calculate the width of the rect for a given time.
	coefficient = max_width / max_time
	time = 0
	dt = 0


	for key in answer['attachments']:
		text = str(key['text']) 
		number_of_words = len(text.split())
		if number_of_words <= 13:   
			api_joke_part_1 = font.render( str(f"{key['text']}"), True, (255, 255, 255)) 
			# Blit on screen 
			screen.fill(BACKGROUND_COLOR)
			screen.blit(api_joke_part_1, (20, 100)) 
		elif number_of_words > 13:
			s1 = text[:len(text)//2] # First half of te text 
			s2 = text[len(text)//2:] # Second half of text 
			api_joke_part_1 = font.render( str(f"{s1}"), True, (255, 255, 255)) 
			api_joke_part_2 = font.render( str(f"{s2}"), True, (255, 255, 255)) 
			# Things to blit on screen 
			screen.fill(BACKGROUND_COLOR) 
			screen.blit(api_joke_part_1, (20, 100)) 
			screen.blit(api_joke_part_2, (20, 150)) 

	done = True 
	while done:

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

		# If mouse is over the button, increase the timer.
		if time < max_time:  # Stop increasing if max_time is reached.
			time += dt
			if time >= max_time:
				time = max_time
		else:  # If not colliding, reset the time.
			time = 0
			done = False  

		width = time * coefficient 

		pg.draw.rect(screen, LIGHT_GRAY, (121, 600, width, 80))
		pg.draw.rect(screen, GRAY, button_rect, 2)

		pg.display.flip()
		dt = clock.tick(60) / 1000
		pg.display.update() 
