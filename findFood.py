import pygame
import time
import random

from agent import Agent

#initailize
pygame.init()

#dimenstions of the window
DISPLAY_WIDTH = 270
DISPLAY_HEIGHT = 270
BLOCK_SIZE = 30

FPS = 30

font = pygame.font.SysFont("ubuntu", 20)
largefont = pygame.font.SysFont(None, 20)

icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)


def draw_snake(snakelist, block_size):
	for x,y in snakelist:
		pygame.draw.rect(gameDisplay, blue, [x, y, block_size, block_size])


def display_score(score):
	text = largefont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [10,10])


def create_text_object(text, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0):
	textSurf, textRect =  create_text_object(msg, color)
	textRect.center = (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2)+y_displace
	gameDisplay.blit(textSurf, textRect)

#Defining colors (rgb values)
BACKGROUND_COLOR = (178, 217, 4)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


#set up the display
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("PyPyper")


clock = pygame.time.Clock()

def initialize_random_position(display_width, display_height, block_size):
	x = random.randrange(0, display_width, step=block_size)
	y = random.randrange(0, display_height, step=block_size)
	# x = round(random.randrange(0, display_width - block_size,)/float(block_size))*block_size
	# y = round(random.randrange(0, display_height - block_size)/float(block_size))*block_size
	# print(x, y)
	return x, y

# Directions
ALLOWED_DIRS = ["LEFT", "RIGHT", "UP", "DOWN"]


class Environment(object):
	def __init__(self,
		         display_width,
		         display_height,
		         block_size,
		         valid_directions):

		self.world_width = display_width
		self.world_height = display_height
		self.block_size = block_size
		self.lead_x, self.lead_y = initialize_random_position(self.world_width, self.world_height, self.block_size)
		self.lead_x_change = 0
		self.lead_y_change = 0
		self.valid_actions = valid_directions

		self.highest_score_so_far = -1

		self.appleX, self.appleY = initialize_random_position(self.world_width, self.world_height, self.block_size)
    

	def act(self, action):
		'''
		Given an action, return the reward.
		'''

		#print("act    : cur pos: (%d, %d), cur direction: %s" % (self.lead_x, self.lead_y, action))
		reward = -1
		is_boundary = self.is_wall_nearby()

		game_end = 0

		if is_boundary[action]:
			reward = -100
			game_end = 1
		else:
			self.move(action)
			if self.is_goal_state(self.lead_x, self.lead_y):
				reward = 100
				game_end = 2
		return reward, game_end

	def move(self, direction):
		x_change = 0
		y_change = 0
		
		if direction in ALLOWED_DIRS:
			if direction == "LEFT":
				x_change = -self.block_size
				y_change = 0
			elif direction == "RIGHT":
				x_change = self.block_size
				y_change = 0
			elif direction == "UP":
				x_change = 0
				y_change = -self.block_size
			elif direction == "DOWN":
				x_change = 0
				y_change = self.block_size
		else:
			print("Invalid direction.")

		self.lead_x += x_change
		self.lead_y += y_change

	def is_wall_nearby(self):
		left, right, up, down = False, False, False, False

		if self.lead_x < self.block_size:
			left = True
			#print('cur x: ', self.lead_x, 'left: ', left)
		if self.lead_x + self.block_size >= self.world_width:
			right = True
		if self.lead_y < self.block_size:
			up = True
		if self.lead_y + self.block_size >= self.world_height:
			down = True

		diction = {"LEFT":left,
					"RIGHT":right,
					"UP":up,
					"DOWN":down}	

		return diction

	def is_apple_nearby(self):
		left, right, up, down = False, False, False, False
		if self.lead_x - self.block_size < self.appleX:
			left = True
		if self.lead_x + self.block_size >= self.appleX:
			right = True
		if self.lead_y - self.block_size < self.appleY:
			up = True
		if self.lead_y + self.block_size >= self.appleY:
			down = True

		return {
			"LEFT":left,
			"RIGHT":right,
			"UP":up,
			"DOWN":down
		}

	def get_state(self):

		head_position = self.get_head_position()
		apple_position = self.get_appple_position()
		apple_info = tuple(self.is_apple_nearby().values())
		wall_info = tuple(self.is_wall_nearby().values())

		#print('wall_info: ', wall_info)
		
		# concatenating the tuples
		#return head_position + apple_position + apple_info + wall_info
		return head_position
		
	def get_next_goal(self):
		return (self.appleX, self.appleY)

	def is_goal_state(self, x, y):
		if (x-self.block_size < self.appleX <x + self.block_size  and 
			y-self.block_size < self.appleY <y + self.block_size):
			return True
		return False

	def get_head_position(self):
		return self.lead_x, self.lead_y

	def update_head_position(self):
		self.lead_x, self.lead_y = initialize_random_position(self.world_width, self.world_height, self.block_size)


	def get_appple_position(self):
		return self.appleX, self.appleY

	def new_apple(self):
		self.appleX, self.appleY = initialize_random_position(self.world_width, self.world_height, self.block_size)

	'''
	def get_apple_quadrant(self):
		appleX, appleY = self.get_appple_position()
		x, y = self.get_head_position()
		quadrant = 0

		#shift the origin
		appleX -= x
		appleY -= y

		if appleX > 0 and appleY > 0: 
			quadrant = 1
		elif appleX < 0 and appleY > 0:
			quadrant = 2
		elif appleX < 0 and appleY < 0:
			quadrant = 3
		elif appleX > 0 and appleY < 0:
			quadrant = 4
		elif appleX == 0:
			if appleY > 0:
				quadrant = random.choice([1, 2])
			if appleY < 0:
				quadrant = random.choice([3, 4])
		elif appleY == 0:
			if appleX > 0:
				quadrant = random.choice([1, 4])
			if appleX < 0:
				quadrant = random.choice([2, 3])
		return quadrant

	def set_high_score(self, val):
		self.highest_score_so_far = val

	def high_score(self):
		return self.highest_score_so_far
	'''

# Initialize the environment	
env = Environment(DISPLAY_WIDTH,
	              DISPLAY_HEIGHT,
	              BLOCK_SIZE,
	              ALLOWED_DIRS)

#print("init snake: (%d, %d) init apple: (%d, %d)"% (env.lead_x, env.lead_y, env.appleX, env.appleY))

agent = Agent(env)

gameExit = False
gameOver = False

snakelist = []
snakeLength = 1

direction = ''

num_episode = 200
max_step = 2000


reward_list = []

running = True

max_score = 0

score = 0
	
episode = 0
	
cur_reward = 0

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
			running = False

	
	direction = agent.get_action()
	#print("get_action: cur pos: (%d, %d), cur direction: %s" % (env.lead_x, env.lead_y, direction))
	
	# Draw apple and background
	gameDisplay.fill(BACKGROUND_COLOR)
	apple = env.get_appple_position()

	if direction:
		
		reward, game_end = env.act(direction)

		agent.update(direction, reward)

		cur_reward += reward
		#print('cur_reward: ', cur_reward)

		# Head of the snake
		snake_head = env.get_head_position()
		snakelist.append(snake_head)
	
		#print("get_head_position: cur pos: (%d, %d), cur direction: %s" % (env.lead_x, env.lead_y, direction))

		if game_end == 1:
			score = 0
		elif game_end == 2:
			env.update_head_position()
			snakelist = []
			snakeLength = 1
			score += 1
			gameOver = True
				#print(agent.q_table)
			# if score > 5:
			# 	break
			#break
				
		
		if len(snakelist) > snakeLength:
			del(snakelist[0])


		pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
		draw_snake(snakelist, BLOCK_SIZE)
		display_score(score)

	pygame.display.update()
	clock.tick(FPS)

	if gameOver:
		episode += 1
		agent.update_exploration(episode)
		print("episode: %d, reward: %d" % (episode, cur_reward))
		cur_reward = 0
		gameOver = False

pygame.quit()