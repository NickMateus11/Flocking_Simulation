import pygame
import time
from random import randint


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ball():
    def __init__(self, start_pos):
        self.pos = Coord(*start_pos)
        self.vy = 0
        self.vx = randint(3,10) * (2*randint(0,1)-1)
        self.trail = []
    
    def pos_tuple(self):
        return (self.pos.x, self.pos.y)

def main():
    g = -1
    r = 10
    dt = 0.05
    
    num_balls = 30
    balls = [Ball( (randint(r,w-r), randint(r,h-r)) ) for _ in range(num_balls)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)

        for b in balls:
            if b.pos.y - (b.vy * dt) > h-r:
                b.vy *= -1

            b.pos.y -= b.vy * dt
            b.vy += g*dt

            b.pos.x += b.vx * dt
            if b.pos.x > w-r or b.pos.x < r:
                b.vx *= -1

            pygame.draw.circle(screen, WHITE, b.pos_tuple(), r, 1)
            b.trail.append(b.pos_tuple()) 

            if len(b.trail) > 2:
                pygame.draw.lines(screen, WHITE, False, b.trail, 1)
            if len(b.trail) > 50:
                b.trail.pop(0)

        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()

