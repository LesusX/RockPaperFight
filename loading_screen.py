import pygame as pg
import requests
import sys 


def start_loading_screen():

	pg.font.init() 
	screen = pg.display.set_mode((1200, 720))
	clock = pg.time.Clock() 
	font = pg.font.Font("assets/font.ttf", 17)
	response = requests.get("https://icanhazdadjoke.com/slack")
	answer = response.json()

	BACKGROUND_COLOR = '#0d0e2e'
	LIGHT_GRAY = '#ff3300' 
	GRAY = '#33cc33'
 
	# Button variables.
	button_rect = pg.Rect(120, 600, 1000, 80)
	max_width = 1000  # Maximum width of the rect.
	max_time = 6  # Time after which the button should be filled.
	# Coefficient to calculate the width of the rect for a given time.
	coefficient = max_width / max_time
	time = 0
	dt = 0

	done = True 
	while done:

		for key in answer['attachments']:
			api_joke = font.render( str(f"{key['text']}"), True, (255, 255, 255))

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

		screen.fill(BACKGROUND_COLOR)
		pg.draw.rect(screen, LIGHT_GRAY, (121, 600, width, 80))
		pg.draw.rect(screen, GRAY, button_rect, 2)
		screen.blit(api_joke, (20, 100))

		pg.display.flip()
		dt = clock.tick(60) / 1000
		pg.display.update()
