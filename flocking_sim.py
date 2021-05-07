import pygame
import time
import math
import random


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GRAY  = pygame.Color(100, 100, 100)

def dist(A, B):
    return ((A[0]-B[0])**2 + (A[1]-B[1])**2)**0.5
def mag(A):
    return dist( (0,0), A)

def draw_arrow(start, end):
    dir_v = (end[0]-start[0], end[1]-start[1])
    if mag(dir_v) < 1:
        return 
    unit_v = (dir_v[0] / mag(dir_v), dir_v[1] / mag(dir_v))

    scale = min(0.2,  (min(w,h) / 10) / mag(dir_v))
    mid_p = ( (end[0] - dir_v[0]*scale), (end[1] - dir_v[1]*scale) )
    arm_mag_perp = dist(end,mid_p) * math.tan(math.pi/6)

    lines = [
        (start, end),
        (end, (-arm_mag_perp*unit_v[1] + mid_p[0],  arm_mag_perp*unit_v[0] + mid_p[1])),
        (end, ( arm_mag_perp*unit_v[1] + mid_p[0], -arm_mag_perp*unit_v[0] + mid_p[1])),
    ]
    for pair in lines:
        pygame.draw.line(screen, WHITE, *pair)

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_tuple(self):
        return (self.x, self.y)

class Bird():
    def __init__(self, start_pos):
        self.pos = Coord(*start_pos)
        self.vy = random.randint(1,5) * (2*random.randint(0,1)-1)
        self.vx = random.randint(1,5) * (2*random.randint(0,1)-1)
        self.trail = []
    
    def pos_tuple(self):
        return (self.pos.to_tuple())

'''
Flocking Rules:
Cohension - birds try to get closer to surrounding groups of birds
Separation - birds avoid colliding
Alignment - align velocity vectors of nearby birds
'''

def cohesion(bird, flock, factor):
    prox = 100
    x = 0
    y = 0
    n = 0
    for b in flock:
        if dist(bird.pos_tuple(), b.pos_tuple()) < prox:
            x += b.pos.x
            y += b.pos.y
            n += 1
    if n:
        x = x/n
        y = y/n
        return (factor*(x - bird.pos.x), factor*(y - bird.pos.y))
    else: 
        return (0 , 0)

def separation(bird, flock, factor):
    x = 0
    y = 0
    for b in flock:
        if bird.pos == b.pos:
            continue
        if dist(bird.pos_tuple(), b.pos_tuple()) < 20:
            x += bird.pos.x - b.pos.x
            y += bird.pos.y - b.pos.y
    return (x*factor, y*factor)

def alignment(bird, flock, factor):
    prox = 100
    x = 0
    y = 0
    n = 0
    for b in flock:
        if dist(bird.pos_tuple(), b.pos_tuple()) < prox:
            x += b.vx
            y += b.vy
            n += 1
    if n:
        x = x/n
        y = y/n
        return (factor*(x - bird.vx), factor*(y - bird.vy))
    else: 
        return (0 , 0)


def main():
    r = 10
    vmax = 15
    slow_down_v = 0.5
    dt = 0.05
    trail = []
    eps = r/2
    dist_error = 0

    coh = 5e-4
    sep = 5e-3
    align = 5e-3

    num_birds = 30
    birds = [Bird( (random.randint(r,w-r), random.randint(r,h-r)) ) for _ in range(num_birds)]

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bird in birds:
            if bird.pos.x + bird.vx*dt > w-4*r:
                bird.vx -= slow_down_v
            if bird.pos.x + bird.vx*dt < 4*r:
                bird.vx += slow_down_v
            if bird.pos.y + bird.vy*dt > h-4*r:
                bird.vy -= slow_down_v 
            if bird.pos.y + bird.vy*dt < 4*r:
                bird.vy += slow_down_v

            v_res = cohesion(bird, birds, coh) + separation(bird, birds, sep) + alignment(bird, birds, align)
            vx = sum(v_res[::2])
            vy = sum(v_res[1::2])
            bird.vx += vx*2
            bird.vy += vy*2

            if abs(bird.vx) > vmax:
                bird.vx = vmax if bird.vx>0 else -vmax
            if abs(bird.vy) > vmax:
                bird.vy = vmax if bird.vy>0 else -vmax

            if abs(bird.vx) < 5 and abs(bird.vy) < 5:
                bird.vx *= 1.1 
                bird.vy *= 1.1

            bird.pos.x += bird.vx*dt
            bird.pos.y += bird.vy*dt

            pygame.draw.circle(screen, WHITE, bird.pos_tuple(), r, 1)      
            
            v_scale = 3*r/vmax
            v_vector = ( bird.pos.x + v_scale*bird.vx, bird.pos.y + v_scale*bird.vy )
            draw_arrow(bird.pos_tuple(), v_vector)

        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()