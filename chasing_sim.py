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
        self.vy = 0
        self.vx = 0
        self.trail = []
    
    def pos_tuple(self):
        return (self.pos.to_tuple())

def main():
    r = 10
    vmax = 5
    dt = 0.05
    kp = 1e-3
    trail = []
    eps = r/2
    dist_error = 0

    num_birds = 3
    birds = [Bird( (random.randint(r,w-r), random.randint(r,h-r)) ) for _ in range(num_birds)]

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bird in birds:
            if bird.pos.x + bird.vx*dt > w-r or bird.pos.x + bird.vx*dt < r:
                bird.vx *= -1
            if bird.pos.y + bird.vy*dt > h-r or bird.pos.y + bird.vy*dt < r:
                bird.vy *= -1

            if dist_error < eps:
                des_pos = Coord(random.randint(r, w-r), random.randint(r, h-r))
            dist_error = ((des_pos.x - bird.pos.x)**2 + (des_pos.y - bird.pos.y)**2)**0.5
            # des_pos = pygame.mouse.get_pos()

            theta = math.atan2(des_pos.y - bird.pos.y, des_pos.x - bird.pos.x)
            errorx = vmax * math.cos(theta) - bird.vx
            errory = vmax * math.sin(theta) - bird.vy
            bird.vx += kp*errorx
            bird.vy += kp*errory

            bird.pos.x += bird.vx*dt
            bird.pos.y += bird.vy*dt

            pygame.draw.circle(screen, WHITE, bird.pos_tuple(), r, 1)   
            pygame.draw.circle(screen, GRAY, des_pos.to_tuple(), 10, 2)     
            
            v_scale = 3*r/vmax
            v_vector = ( bird.pos.x + v_scale*bird.vx, bird.pos.y + v_scale*bird.vy )
            draw_arrow(bird.pos_tuple(), v_vector)

        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()

