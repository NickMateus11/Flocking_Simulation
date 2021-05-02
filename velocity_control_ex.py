import pygame
import time
import math


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

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

def main():
    vx = 0
    vy = 0
    vmax = 10
    r = 10
    dt = 0.05
    d_speed = 0.05
    pos = [w/2, h/2]
    trail = []

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_LEFT]:
            vx += -d_speed
        if keyPressed[pygame.K_RIGHT]:
            vx += d_speed
        if keyPressed[pygame.K_UP]:
            vy += -d_speed
        if keyPressed[pygame.K_DOWN]:
            vy += d_speed     

        if abs(vx) > vmax:
            vx = vmax if vx>0 else -vmax
        if abs(vy) > vmax:
            vy = vmax if vy>0 else -vmax

        pos[1] += vy*dt
        vy -= d_speed*vy*dt 

        pos[0] += vx*dt
        vx -= d_speed*vx*dt 

        v_scale = 5*r/vmax
        v_vector = ( pos[0] + v_scale*vx, pos[1] + v_scale*vy )
        draw_arrow(pos, v_vector)

        pygame.draw.circle(screen, WHITE, pos, r, 1)

        # if (abs(vy)>0.5 or abs(vx)>0.5):
        #     trail.append(tuple(pos))

        # if len(trail) > 2:
        #     pygame.draw.lines(screen, WHITE, False, trail, 1)
        # if len(trail) > 50 or (trail and abs(vy)<0.5 and abs(vx)<0.5):
        #     trail.pop(0)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()

