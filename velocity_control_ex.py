import pygame
import time


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

def main():
    vx = 0
    vy = 0
    vmax = 10
    r = 10
    pos = [w/2, h/2]
    points = []

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        time.sleep(0.1)
        
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_LEFT]:
            vx += -2
        if keyPressed[pygame.K_RIGHT]:
            vx += 2
        if keyPressed[pygame.K_UP]:
            vy += -2
        if keyPressed[pygame.K_DOWN]:
            vy += 2      

        if abs(vx) > vmax:
            vx = vmax if vx>0 else -vmax
        if abs(vy) > vmax:
            vy = vmax if vy>0 else -vmax

        pos[1] += vy
        vy *= 0.7

        pos[0] += vx
        vx *= 0.7

        pygame.draw.circle(screen, WHITE, pos, r, 1)
        points.append(tuple(pos))

        if len(points) > 2:
            pygame.draw.lines(screen, WHITE, False, points, 1)
        if len(points) > 20:
            points.pop(0)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()

