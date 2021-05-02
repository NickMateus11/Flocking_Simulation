import pygame
import time


w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

def main():
    g = -1
    v = 0
    hv = 5
    r = 10
    pos = [0, h]
    points = []

    running = True
    while running:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)

        if pos[1]-v > h-r:
            v = 20

        pos[1] -= v
        v += g

        pos[0] += hv

        pygame.draw.circle(screen, WHITE, pos, r, 1)
        points.append(tuple(pos))
        if pos[0]+hv > w-r or pos[0]+hv < r:
            hv *= -1

        if len(points) > 2:
            pygame.draw.lines(screen, WHITE, False, points, 1)
        if len(points) > 100:
            points.pop(0)

        pygame.display.flip()
    
    pygame.quit()


if __name__ == '__main__':
    main()

