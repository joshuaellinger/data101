# to run:
#   1. pip install pygbag
#   2. (optional) add the scripts directory to your path if missing
#   3. cd ./browser
#   4. type pygbag.exe .\main.py
#   5. open a web page at http://localhost:8000

import pygame
import random
import asyncio
import time

from ui import *

# Initialize pygame
pygame.init()

pygame.display.set_caption("Moving Circle")

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CIRCLE_RADIUS = 15

SPEED = 5
INC_SPEED = 1
MAX_SPEED = 50

# Colors
RED = (255, 0, 0)
COLORS = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Global variables
#circle_x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
#circle_y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)
circle_x = SCREEN_WIDTH // 2
circle_y = SCREEN_HEIGHT // 2
circle_dx = SPEED
circle_dy = 0
circle_color = RED
running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Circle")
clock = pygame.time.Clock()


async def main():
    global circle_x, circle_y, circle_dx, circle_dy, circle_color, running

    fps = 10
    delay_ns = int(1e9/fps)

    print("run")
    count = 0

    ts = time.time_ns()
    while running:
        
        # check if we have at least 100ms between updates
        ts2 = time.time_ns()
        d = ts2 - ts
        if d < delay_ns: 
            redraw = False
        else:
            redraw = True
            ts = ts2

        if redraw:
            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw the circle
            pygame.draw.circle(screen, circle_color, (circle_x, circle_y), CIRCLE_RADIUS)

            # Move the circle
            circle_x += circle_dx
            circle_y += circle_dy

            # Check for wall collision
            if circle_x - CIRCLE_RADIUS <= 0 or circle_x + CIRCLE_RADIUS >= SCREEN_WIDTH:
                circle_dx = -circle_dx
            if circle_y - CIRCLE_RADIUS <= 0 or circle_y + CIRCLE_RADIUS >= SCREEN_HEIGHT:
                circle_dy = -circle_dy


        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                distance = ((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2) ** 0.5
                if distance <= CIRCLE_RADIUS:
                    circle_dx = -circle_dx
                    circle_color = random.choice([c for c in COLORS if c != circle_color])
            if event.type == pygame.KEYDOWN:
                key = event.dict["key"]
                if key == pygame.K_UP:
                    circle_dy = max(circle_dy - INC_SPEED, 0) 
                elif key == pygame.K_DOWN: 
                    circle_dy = min(circle_dy + INC_SPEED, MAX_SPEED) 
                elif key == pygame.K_LEFT: 
                    circle_dx = max(circle_dx - INC_SPEED, 0)
                elif key == pygame.K_RIGHT: 
                    circle_dx = min(circle_dx + INC_SPEED, MAX_SPEED) 
                elif key == pygame.K_SPACE:
                    running = False
                

        if redraw:
            pygame.display.flip()

        count += 1
        if count % 10 == 0:
            print(f"wait {count}")
        await asyncio.sleep(0.05)  # Let other tasks run

# This is the program entry point
asyncio.run(main())