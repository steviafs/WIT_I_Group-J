
import pygame
from sys import exit
from random import randint, choice

class Pemain(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		pemain_1 = pygame.image.load('graphics/player/player_run_03.png').convert_alpha()
		pemain_2 = pygame.image.load('graphics/player/player_run_04.png').convert_alpha()
		self.pemain_lari = [pemain_1,pemain_2]
		self.pemain_index = 0
		self.pemain_lompat = pygame.image.load('graphics/player/player_run_04.png').convert_alpha()

		self.image = self.pemain_lari[self.pemain_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravitasi = 0

		self.suara_lompat = pygame.mixer.Sound('audio/jump.mp3')
		self.suara_lompat.set_volume(0.5)

	def input_pemain(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravitasi = -20
			self.suara_lompat.play()

	def gravitasi1(self):
		self.gravitasi += 1
		self.rect.y += self.gravitasi
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animasi1(self):
		if self.rect.bottom < 300: 
			self.image = self.pemain_lompat
		else:
			self.pemain_index += 0.1
			if self.pemain_index >= len(self.pemain_lari):self.pemain_index = 0
			self.image = self.pemain_lari[int(self.pemain_index)]

	def update(self):
		self.input_pemain()
		self.gravitasi1()
		self.animasi1()

class Rintangan(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'virust':
			virust_5 = pygame.image.load('graphics/fly/virus5.png').convert_alpha()
			virust_6 = pygame.image.load('graphics/fly/virus6.png').convert_alpha()
			virust_7 = pygame.image.load('graphics/fly/virus7.png').convert_alpha()
			virust_8 = pygame.image.load('graphics/fly/virus8.png').convert_alpha()
			self.frames = [virust_5,virust_6,virust_7,virust_8]
			y_pos = 150
		elif type == 'virusb':
			virusb_1 = pygame.image.load('graphics/bawah/virus1.png').convert_alpha()
			virusb_2 = pygame.image.load('graphics/bawah/virus2.png').convert_alpha()
			virusb_3 = pygame.image.load('graphics/bawah/virus3.png').convert_alpha()
			virusb_4 = pygame.image.load('graphics/bawah/virus4.png').convert_alpha()
			self.frames = [virusb_1,virusb_2,virusb_3,virusb_4]
			y_pos  = 310
		else:
			virusteng_1 = pygame.image.load('graphics/bawah/virus1.png').convert_alpha()
			virusteng_2 = pygame.image.load('graphics/fly/virus5.png').convert_alpha()
			self.frames = [virusteng_1,virusteng_2]
			y_pos  = 275

		self.index_animasi = 0
		self.image = self.frames[self.index_animasi]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animasi1(self):
		self.index_animasi += 0.1 
		if self.index_animasi >= len(self.frames): self.index_animasi = 0
		self.image = self.frames[int(self.index_animasi)]

	def update(self):
		self.animasi1()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def nilai_skor():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def rintangan_virus(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 5

			if obstacle_rect.bottom == 300: screen.blit(virusb_surf,obstacle_rect)
			elif obstacle_rect.bottom == 150: screen.blit(virust_surf,obstacle_rect)
			else : screen.blit(virusteng_surf,obstacle_rect)
                
		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(player,obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

def player_animation():
	global player_surf, pemain_index

	if player_rect.bottom < 300:
		player_surf = pemain_lompat
	else:
		pemain_index += 0.1
		if pemain_index >= len(pemain_lari):pemain_index = 0
		player_surf = pemain_lari[int(pemain_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Fight Coronavirus')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Pemain())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Background_2a.png').convert()
ground_surface = pygame.image.load('graphics/ground2.png').convert()


# Virus bawah 
virusb_frame_1 = pygame.image.load('graphics/bawah/virus1.png').convert_alpha()
virusb_frame_2 = pygame.image.load('graphics/bawah/virus2.png').convert_alpha()
virusb_frames = [virusb_frame_1, virusb_frame_2]
virusb_frame_index = 0
virusb_surf = virusb_frames[virusb_frame_index]

# Virus terbang
virust_frame1 = pygame.image.load('graphics/fly/virus5.png').convert_alpha()
virust_frame2 = pygame.image.load('graphics/fly/virus6.png').convert_alpha()
virust_frames = [virust_frame1, virust_frame2]
virust_frame_index = 0
virust_surf = virust_frames[virust_frame_index]

#virus tengah
virusteng_frame1 = pygame.image.load('graphics/bawah/virus1.png').convert_alpha()
virusteng_frame2 = pygame.image.load('graphics/fly/virus5.png').convert_alpha()
virusteng_frames = [virusteng_frame1, virusteng_frame2]
virusteng_frame_index = 0
virusteng_surf = virusteng_frames[virusteng_frame_index]

obstacle_rect_list = []


pemain_1 = pygame.image.load('graphics/player/player_run_03.png').convert_alpha()
pemain_2 = pygame.image.load('graphics/player/player_run_04.png').convert_alpha()
pemain_lari = [pemain_1,pemain_2]
pemain_index = 0
pemain_lompat = pygame.image.load('graphics/player/player_run_04.png').convert_alpha()


player_surf = pemain_lari[pemain_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0


# Tampilan Awal

#bg_virus1 = pygame.image.load('graphics/bg1.png').convert()

player_stand = pygame.image.load('graphics/player/bumi.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,1)
player_stand_rect = player_stand.get_rect(center = (400,200))

player2_stand = pygame.image.load('graphics/player/virus2_bg.png').convert_alpha()
player2_stand_rect = player2_stand.get_rect(center = (180,250))

player3_stand = pygame.image.load('graphics/player/virus2_bg.png').convert_alpha()
player3_stand_rect = player3_stand.get_rect(center = (580,150))

"""
bg_virus1 = pygame.image.load('graphics/bg1.png').convert_alpha()
bg_virus1 = pygame.transform.rotozoom(bg_virus1,0,1)
bg_virus1_rect = bg_virus1.get_rect(0,0)
"""

game_name = test_font.render('Fight Coronavirus',False,(250,128,144))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to Fight!',False,(250,128,144))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

virusb_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(virusb_animation_timer,500)

virust_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(virust_animation_timer,200)

virusteng_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(virusteng_animation_timer,100)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
					player_gravity = -20
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 1000)

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Rintangan(choice(['virust','virusb','virusb','virusteng','virusb','virusteng', 'virust'])))


			if event.type == virusb_animation_timer:
				if virusb_frame_index == 0: virusb_frame_index = 1
				else: virusb_frame_index = 0
				virusb_surf = virusb_frames[virusb_frame_index] 

			if event.type == virust_animation_timer:
				if virust_frame_index == 0: virust_frame_index = 1
				else: virust_frame_index = 0
				virust_surf = virust_frames[virust_frame_index] 

			if event.type == virusteng_animation_timer:
				if virusteng_frame_index == 0: virusteng_frame_index = 1
				else: virusteng_frame_index = 0
				virusteng_surf = virusteng_frames[virusteng_frame_index] 

	if game_active:
		screen.blit(sky_surface,(0,-100))
		screen.blit(ground_surface,(0,300))

		score = nilai_skor()
		

		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		# Rintangan movement 
		# obstacle_rect_list = rintangan_virus(obstacle_rect_list)

		# collision 
		game_active = collision_sprite()
		# game_active = collisions(player_rect,obstacle_rect_list)
		
	else:
		screen.fill((255,255,255))
		screen.blit(player_stand,player_stand_rect)
		screen.blit(player2_stand,player2_stand_rect)
		screen.blit(player3_stand,player3_stand_rect)
		#screen.blit(bg_virus1,bg_virus1_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)
		player_gravity = 0

		score_message = test_font.render(f'Your score: {score}',False,(255,0,0))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
