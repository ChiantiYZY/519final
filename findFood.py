import pygame
import time
import random

from agent import Agent

#initailize
pygame.init()

#dimenstions of the window
DISPLAY_WIDTH = 210
DISPLAY_HEIGHT = 210
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
    

	def act(self, action, snakelist):
		'''
		Given an action, return the reward.
		'''

		#print("act    : cur pos: (%d, %d), cur direction: %s" % (self.lead_x, self.lead_y, action))
		reward = -1
		is_boundary = self.is_wall_nearby()
		is_itself = self.is_touching_itself(snakelist)



		game_end = 0

		# if is_boundary[action] or is_itself:
		# 	reward = -100
		# 	game_end = 1

		if is_itself[action]:
			#print('hit itself at direction ', action)
			#print('head: ', (self.lead_x, self.lead_y))
			reward = -100
			game_end = 1
		# 	pass
		elif is_boundary[action]:
			reward = -100
			game_end = 1
		else:
			self.move(action)
			if self.is_goal_state(self.lead_x, self.lead_y):
				self.new_apple()
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

	def is_touching_itself(self, snakelist):
		left, right, up, down = False, False, False, False

		length = len(snakelist)
		maxLen = 4 

		#print('lead pos: ', (self.lead_x, self.lead_y))

		#left
		if (self.lead_x - self.block_size, self.lead_y) in snakelist[0 : length - 1]:
			#print('left bite at pos: ', (self.lead_x - self.block_size, self.lead_y))
			left = True
		if (self.lead_x + self.block_size, self.lead_y) in snakelist[0 : length - 1]:
			#print('right bite at pos: ', (self.lead_x + self.block_size, self.lead_y))
			right = True
		if (self.lead_x, self.lead_y - self.block_size) in snakelist[0 : length - 1]:
			#print('up bite at pos: ', (self.lead_x, self.lead_y - self.block_size))
			up = True
		if (self.lead_x, self.lead_y + self.block_size) in snakelist[0 : length - 1]:
			#print('down bite at pos: ', (self.lead_x, self.lead_y + self.block_size))
			down = True


		# if(left or right or up or down):
		# 	print(snakelist)

		diction = {"LEFT":left,
					"RIGHT":right,
					"UP":up,
					"DOWN":down}	

		return diction

		# if len(snakelist) > 0 and snakelist.count(snakelist[0]) > 1:
		# 	return True
		# return False

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

	def get_state(self, snakelist):

		head_position = self.get_head_position()
		apple_position = self.get_apple_position()
		apple_info = tuple(self.is_apple_nearby().values())
		wall_info = tuple(self.is_wall_nearby().values())
		snake_info = tuple(self.is_touching_itself(snakelist).values())

		relative_pos = (head_position[0] - apple_position[0], head_position[1] - apple_position[1])

		if len(snakelist) > 0:
			tail_head_pos = (snakelist[0][0] - snakelist[-1][0], snakelist[0][1] - snakelist[-1][1])
		else:
			tail_head_pos = (0, 0)

		#print('wall_info: ', wall_info)
		
		# concatenating the tuples
		#return head_position + apple_position + apple_info + wall_info
		#return head_position
		#return relative_pos + wall_info + tail_head_pos
		return relative_pos + wall_info + snake_info
		
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


	def get_apple_position(self):
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

wins = 0
steps = 0
win_count = []
step_count = []

maxLen = 5

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
			running = False

	
	direction = agent.get_action(snakelist)
	#print("get_action: cur pos: (%d, %d), cur direction: %s" % (env.lead_x, env.lead_y, direction))
	
	# Draw apple and background
	gameDisplay.fill(BACKGROUND_COLOR)
	apple = env.get_apple_position()

	if direction:
		
		reward, game_end = env.act(direction, snakelist)

		agent.update(direction, reward, snakelist)

		cur_reward += reward
		#print('cur_reward: ', cur_reward)

		# Head of the snake
		snake_head = env.get_head_position()
		snakelist.append(snake_head)

	
		#print("get_head_position: cur pos: (%d, %d), cur direction: %s" % (env.lead_x, env.lead_y, direction))

		if game_end == 1:
			score = 0
			snakelist = []
			snakeLength = 1
		elif game_end == 2:
			#env.update_head_position()
			#snakelist = []
			snakeLength += 1
			snakeLength = min(snakeLength, maxLen)
			score += 1
			gameOver = True
				#print(agent.q_table)
			# if score > 5:
			# 	break
			#break
				
		
		if len(snakelist) > snakeLength:
			del(snakelist[0])


		#print(snakelist)


		pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], BLOCK_SIZE, BLOCK_SIZE])
		draw_snake(snakelist, BLOCK_SIZE)
		display_score(score)

	pygame.display.update()
	clock.tick(FPS)

	# if gameOver:
	# 	episode += 1
	# 	agent.update_exploration(episode)
	# 	if score % 5 == 0:
	# 		win_count.append(wins)
	# 		step_count.append(steps)
	# 		#print("episode: %d, reward: %d" %(episode, cur_reward))
	# 		print("steps: %d, wins: %d" %(steps, wins))
	# 		steps = 0
	# 	cur_reward = 0
	# 	gameOver = False


	if gameOver:
		episode += 1
		# if episode == 1000:
		# 	break
		steps += 1
		
		
		agent.update_exploration(episode)

		#print('exploration rate: ', agent.exploration_rate)

		if score % 10 == 0:
			wins += 1
			win_count.append(wins)
			step_count.append(steps)
			#print("episode: %d, reward: %d" %(episode, cur_reward))
			print("steps: %d, wins: %d" %(steps, wins))
			steps = 0
		cur_reward = 0
		gameOver = False

pygame.quit()