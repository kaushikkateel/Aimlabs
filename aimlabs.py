import pygame, sys, random, math
from pygame import mixer

class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.score = 0
        self.life = 5
        self.hit = True

    def emit(self):
	    if self.particles:
		    self.delete_particles()
		    for particle in self.particles:
			    particle[1] -= 0.15
			    pygame.draw.circle(screen,pygame.Color('White'),particle[0], int(particle[1]))

    def add_particles(self):
	    pos_x = random.randrange(1280-35)
	    pos_y = random.randrange(720-35)
	    radius = 30
	    particle_circle = [[pos_x,pos_y],radius]
	    self.particles.append(particle_circle)

    def delete_particles(self):
	    particle_copy = [particle for particle in self.particles if particle[1] > 0]
	    self.particles = particle_copy

    def destroy_particle(self, m_x, m_y):
        survived_particle = []
        for particle in self.particles:
            dist = math.sqrt((particle[0][0]-m_x)**2 + (particle[0][1]-m_y)**2)
            # print(dist, particle[1])
            if dist > particle[1]:
                survived_particle.append(particle)
            else:
                sounds = ["data/audio/sound1.mp3","data/audio/sound2.mp3"]
                sound = mixer.Sound(random.choice(sounds))
                sound.set_volume(0.1)
                sound.play()
                self.score += 1
                self.hit = True
        # print(survived_particle)
        self.particles = survived_particle

    def show_score(self, score_x, score_y):
        font = pygame.font.Font('data/assets/advanced-pixel-7-font/advanced_pixel-7.ttf',32)
        score2 = font.render("Score: "+ str(self.score), True, (255, 255, 255))
        screen.blit(score2,(score_x, score_y))

    def show_life(self):
        for heart in range((self.life + 1)):
            screen.blit(full_heart,(1280-(heart*50), 20))

    def hit_or_miss(self):
        if self.hit == False :
            self.life -= 1
        self.hit = False
        # print(self.life)

    def game_over(self):
        if self.life == 0 :
            return True, self.score
        else:
            return False, self.score

    def reset(self):
        self.particles = []
        self.score = 0
        self.life = 5
        self.hit = True


pygame.init()
# monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
monitor_size = [1280,720]
# print(monitor_size)
screen = pygame.display.set_mode(monitor_size)
pygame.display.set_caption('Aimlabs')
clock = pygame.time.Clock()

score_x = 10
score_y = 10

particle1 = ParticlePrinciple()
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,1000)

pygame.mouse.set_cursor(pygame.cursors.broken_x)
gameRun = True
gameOver = False
final_score = 0

full_heart = pygame.image.load('data/assets/full_heart.png').convert_alpha()

def show_gameOver(final_score):
    screen.fill((30,30,30))
    w,h = pygame.display.get_surface().get_size()
    font = pygame.font.Font('data/assets/advanced-pixel-7-font/advanced_pixel-7.ttf',128)
    GO = font.render("GAMEOVER", True, (255, 255, 255))
    GO_rect = GO.get_rect(center=(w/2, h/4))
    screen.blit(GO,GO_rect)

    font = pygame.font.Font('data/assets/advanced-pixel-7-font/advanced_pixel-7.ttf',64)
    Fscore = font.render("SCORE: "+str(final_score), True, (255, 255, 255))
    Fscore_rect = Fscore.get_rect(center=(w/2, h/2))
    screen.blit(Fscore,Fscore_rect)

    font = pygame.font.Font('data/assets/advanced-pixel-7-font/advanced_pixel-7.ttf',32)
    play_again = font.render("Press SPACE to play again", True, (255, 255, 255))
    play_again_rect = play_again.get_rect(center=(w/2, h/(4/3)))
    screen.blit(play_again ,play_again_rect)
    
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

while gameRun:
    if gameOver:
        show_gameOver(final_score)
        gameOver = False
        particle1.reset()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
            particle1.hit_or_miss()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            sounds = ["data/audio/sound4.mp3","data/audio/sound5.mp3"]
            sound = mixer.Sound(random.choice(sounds))
            sound.set_volume(0.1)
            sound.play()
            m_x, m_y = pygame.mouse.get_pos()
            particle1.destroy_particle(m_x, m_y)


    screen.fill((30,30,30))
    particle1.emit()
    gameOver, final_score = particle1.game_over()
    particle1.show_life()
    particle1.show_score(score_x, score_y)
    pygame.display.update()
    clock.tick(120)