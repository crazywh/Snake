import pygame, sys, os
from pygame.locals import *
from random import *

# 窗口打开位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "300, 100"

# 初始化
pygame.init()
pygame.mixer.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("贪吃蛇")
font = pygame.font.SysFont("impact", 32)
font1 = pygame.font.SysFont("impact", 20)
# 查看系统字体
# print(pygame.font.get_fonts())

# 小格宽度
CLIESIZE = 20
# cell = (CLIESIZE, CLIESIZE)
# 横纵格子数
x_num = int(w // CLIESIZE)
y_num = int(h // CLIESIZE)

# 加载音乐
pygame.mixer.music.load('sound/bg.mp3')
pygame.mixer.music.set_volume(0.5)

# 定义颜色
BLACK = (0, 0, 0)
WHITE1 = (255, 255, 255)
WHITE2 = (50, 50, 50)
BULE = (0, 0, 125)
RED = (255, 0, 0)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 125, 0)

# 定义运行方向
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

# 功能函数
def draw_rect():
	for i in range(1, x_num):
		pygame.draw.line(screen, WHITE2, (i * CLIESIZE, 20), (i * CLIESIZE, h), 1)
	for i in range(1, y_num):
		pygame.draw.line(screen, WHITE2, (0, i * CLIESIZE), (w, i * CLIESIZE), 1)

def draw_apple(apple_coord):
	pygame.draw.rect(screen, RED, (apple_coord[0] * CLIESIZE, apple_coord[1] * CLIESIZE, CLIESIZE, CLIESIZE), 0)

def get_apple_coord(snake_coords):
	x = randint(0, x_num - 1)
	y = randint(1, y_num - 1)
	while [x, y] in snake_coords:
		x = randint(0, x_num - 1)
		y = randint(1, y_num - 1)
	return [x, y]
	
def draw_snake(snake_coords):
	for i in snake_coords[1:]:
		pygame.draw.rect(screen, GREEN1, (i[0] * CLIESIZE, i[1] * CLIESIZE, CLIESIZE, CLIESIZE), 0)
		pygame.draw.rect(screen, GREEN2, (i[0] * CLIESIZE, i[1] * CLIESIZE, CLIESIZE, CLIESIZE), 3)
	pygame.draw.rect(screen, BULE, (snake_coords[0][0] * CLIESIZE, snake_coords[0][1] * CLIESIZE, CLIESIZE, CLIESIZE), 0)
	pygame.draw.rect(screen, GREEN2, (snake_coords[0][0] * CLIESIZE, snake_coords[0][1] * CLIESIZE, CLIESIZE, CLIESIZE), 3)

def print_text(font, x, y, text, color = WHITE1):
	ti = font.render(text, True, color)
	screen.blit(ti, (x, y))

def main():
	# 游戏开始界面
	screen.fill(BLACK)
	draw_rect()
	draw_snake([[21, 15], [20, 15], [19, 15], [18, 15]])
	print_text(font1, 300, 400, "Press  Space  to  Start !")
	pygame.display.update()
	pygame.mixer.music.play(-1)
	clock = pygame.time.Clock()
	# 贪吃蛇初始位置,几组坐标就代表有几段
	snake_coords = [[21, 15], [20, 15], [19, 15], [18, 15]]
	head = snake_coords[0]
	direction = RIGHT
	# 苹果初始位置
	apple_coord = [randint(30, 35), randint(20, 25)]
	# 音乐控制
	sound = True
	# 游戏难度
	level = 5
	# 记录分数
	score = 0
	recorded = False
	# 游戏运行控制
	pause =  True
	gameover = False	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key in [K_RIGHT, K_d] and direction not in [1, 2] and not pause:
					direction = RIGHT
				elif event.key in [K_LEFT, K_a] and direction not in [1, 2] and not pause:
					direction = LEFT
				elif event.key in [K_UP, K_w] and direction not in [3, 4] and not pause:
					direction = UP
				elif event.key in [K_DOWN, K_s] and direction not in [3, 4] and not pause:
					direction = DOWN
				elif event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_SPACE:
					pause = not pause
					# sound = not sound
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					pos = event.pos
					if 40 < pos[0] < 120 and 0 < pos[1] < 20:
						sound = not sound
		# 音乐控制
		if sound and not pause:
			pygame.mixer.music.unpause() 
		else:
			pygame.mixer.music.pause()
		if not pause:
			# 贪吃蛇运动
			if direction == RIGHT:
				head = [head[0] + 1, head[1]]
			elif direction == LEFT:
				head = [head[0] - 1, head[1]]
			elif direction == UP:
				head = [head[0], head[1] - 1]
			elif direction == DOWN:
				head = [head[0], head[1] + 1]

			if head in snake_coords or head[0] < 0 or head[1] < 0 or head[0] >= x_num or head[1] >= y_num:
				gameover = True 
			elif head == apple_coord:
				snake_coords.insert(0, head)
				apple_coord = get_apple_coord(snake_coords)
				score = len(snake_coords) - 4
			else:
				snake_coords.insert(0, head)
				snake_coords.pop()

			if 10 < score <= 20:
				level = 7
			elif 20 < score <= 30:
				level = 10
			elif 30 < score < 50:
				level = 13
			elif score > 50:
				level = 20
			screen.fill(BLACK)
			if not gameover:
				draw_rect()
				draw_snake(snake_coords)
				draw_apple(apple_coord)
				print_text(font1, 700, 0, "Score: " + str(score))
				if sound:
					print_text(font1, 40, 0, "Sound: On")
				else:
					print_text(font1, 40, 0, "Sound: Off")	

		if gameover:
			screen.fill(BLACK)
			if not recorded:
				recorded = True
				with open('record.txt', 'r') as f:
					record_score = int(f.read())
				if record_score < score:
					with open('record.txt', 'w') as f:
						f.write(str(score))

			pygame.mixer.music.stop()
			print_text(font, 300, 150, "  GAME OVER! ")
			print_text(font, 300, 200, "Best Score:  " + str(record_score))
			print_text(font, 300, 250, "Your Score:  " + str(score))
			print_text(font, 280, 350, "Restart" )
			print_text(font, 450, 350, "Exit" )
			# 玩家选择
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				if 280 < pos[0] < 376 and 350 < pos[1] < 390:
					main()
				elif 450 < pos[0] < 494 and 350 < pos[1] < 390:
					sys.exit()	
		
		pygame.display.update()
		clock.tick(level)		

if __name__ == "__main__":
	main()