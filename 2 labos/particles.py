import pygame, sys, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480


def main():
	global FPSCLOCK, DISPLAY
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption("2. laboratorijska vjezba iz Racunalne animacije")

	num_particles = 50
	start_width = WINDOWWIDTH
	start_height = 0

	particles = []
	while num_particles > 0:
		# particles elements:
		# x = 0
		# y = 1
		# size = 2
		# direction = 3
		# flag = 4
		# addition = 5
		# color = 6
		# influence = 7
		particles.append([start_width, start_height, 0, 0, (0, 0), 0, (0, 0, 0), (0, 0), 0, 0])
		num_particles -= 1
	
	velocity = []
	random_size = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
	random_direction = [1, 2]
	start_color = (0, 0, 240)
	for particle in particles:
		particle[2] = random.sample(random_size, 1)[0]
		particle[3] = random.sample(random_direction, 1)[0]
		particle[6] = start_color
		particle[7] = (random.randint(1, 5), random.randint(1, 5))
		velocity.append(random.randint(1, 3))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()

		DISPLAY.fill((0, 0, 0))
		# DRAW PARTICLES

		for element in range(len(particles)):
			particle_x = particles[element][0]
			particle_y = particles[element][1]
			size = particles[element][2]
			direction = particles[element][3]
			flag = particles[element][4][0]
			minus = particles[element][4][1]
			time = particles[element][5]
			color = particles[element][6]
			color2 = (240,0,0)

			influence = particles[element][7]
			particle2_x = particles[element][8]
			particle2_y = particles[element][9]

			particle_x += (velocity[element] * time * influence[0]) * (-1*direction)
			particle_y += (velocity[element] * time * influence[1]) * (direction)
			particle2_x += (velocity[element] * time * influence[0]) * (direction)
			particle2_y += (velocity[element] * time * influence[1]) * (direction)



			pygame.draw.circle(DISPLAY, color, (int(particle_x), int(particle_y)), int(size))
			pygame.draw.circle(DISPLAY, color2, (int(particle2_x), int(particle2_y)), int(size))


			if (flag == 0) and (size > 0):
				steps = size*2
				minus = 240/steps
				new = (1, minus)

				particles[element][4] = new

			if (size > 0):
				particles[element][2] -= 0.5
				boja = color[2] - minus
				color2 = (color2[0]-minus,0,0)
				particles[element][6] = (0,0,boja)
				particles[element][5] += 1
			else:
				particles[element][0] = WINDOWWIDTH
				particles[element][1] = start_height
				particles[element][2] = random.sample(random_size, 1)[0]
				particles[element][3] = random.sample(random_direction, 1)[0]
				particles[element][4] = (0,0)
				particles[element][5] = 0
				particles[element][6] = (0, 0, 240)
				particles[element][7] = (random.randint(1,5), random.randint(1,5))	
				particles[element][8] = 0
				particles[element][9] = start_height
				velocity[element] = random.randint(1, 3)
				
		pygame.display.update()
		FPSCLOCK.tick(FPS)


if __name__ == '__main__':
	main()