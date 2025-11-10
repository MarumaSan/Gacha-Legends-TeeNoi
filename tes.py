import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# fake item
item = pygame.Rect(300, 250, 80, 80)
dragging = False
offset_x = 0
offset_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()

        # click down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if item.collidepoint(event.pos):
                dragging = True
                # mouse_x, mouse_y = event.pos
                # offset_x = item.x - mouse_x

        # release mouse
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # drag move
        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            item.x = mouse_x + offset_x

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 200, 50), item)
    pygame.display.flip()
    clock.tick(60)
