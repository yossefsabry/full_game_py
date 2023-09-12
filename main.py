# start full game

import pygame
import os

pygame.init()

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# caption
pygame.display.set_caption("Shooter || Yossef")

# set framerate
clock = pygame.time.Clock()
FBS = 60

# define game veriables
GRAVITY = 0.75

# define player section verables
moving_left = False
moving_right = False

# colors
RED = (255,0,0)

def draw_bg():
	SCREEN.fill((0,100,0))
	pygame.draw.line(SCREEN, RED, (0, 300), (SCREEN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.char_type = char_type
		self.alive = True
		self.speed = speed
		self.scale = scale
		self.direction = 1
		self.jump = False
		self.in_air = True
		self.vel_y = 0
		self.animation_list = []
		self.frame_index = 0
		self.flip = False # use for flip img using transform if true the filp while in x axis if false there is no flip
		self.action_index = 0
		# for update time for animation list
		self.update_time = pygame.time.get_ticks()
		
		# load all animation for the player
		animation_type = ["Idle", "Run", "Jump"]
		for animation in animation_type:
			temp_list = []
			# count for the number for image in the folder for every animation
			num_of_num = len(os.listdir(f"img/{self.char_type}/{animation}"))
			for i in range(num_of_num):
				img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png")
				img = pygame.transform.scale(img,(int(img.get_width() * scale),int(img.get_height()* scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action_index][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def move(self, moving_left, moving_right):
		# assign movement varables if moving right or left
		# movement variables for collistion
		dx = 0 
		dy = 0 
		if  moving_left:
			dx = -self.speed 
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		# jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		# apply gravity
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		# temprarey collistion line and  player
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False  



		# update rectangle possition
		self.rect.x += dx
		self.rect.y += dy

	def update_animation(self):
		# update animation
		ANIMATION_COOLDOWN = 100
		# update image depending on current frame
		self.image = self.animation_list[self.action_index][self.frame_index]
		# check if eneough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			# must rest the time to start from start
			self.update_time = pygame.time.get_ticks()
			# next image
			self.frame_index += 1

		# rest the index (index out of range)
		if self.frame_index >= len(self.animation_list[self.action_index]):
			self.frame_index = 0

	def update_action(self, new_action):
		# first check for the inidex_action is equl to new_action
		if self.action_index != new_action:
			self.action_index = new_action
			# update all settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()


	def draw(self):
		SCREEN.blit(pygame.transform.flip(self.image, self.flip,False),  self.rect)




player = Soldier('player',200, 200, 2, 5)
enemy = Soldier('enemy',500, 200, 2, 5)


run = True
while run:
	draw_bg()
	clock.tick(FBS)

	
	player.update_animation()
	enemy.draw()
	player.draw()
	# animation move
	if player.alive:
		if player.in_air:
			player.update_action(2) # 2 => main player jump
		elif moving_left or moving_right:
			player.update_action(1) # 1 => main player move
		else:
			player.update_action(0) # 0 => main player standing
			
	player.move(moving_left, moving_right)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		# keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False

		# keyboard presses
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
	
	pygame.display.update()

pygame.quit() 
