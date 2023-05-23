import pygame

def display_placement(lst, window, scroll):
    font = pygame.font.Font(None, 48)
    x = 0
    y = 20 - scroll
    interval = 30
    for i in range(len(lst)):
        text = font.render(str(i + 1), True, (0, 0, 0))
        window.blit(text, (x, y))
        y += interval

def display_tag(lst, window, scroll):
    font = pygame.font.Font(None, 48)
    x = 80
    y = 20 - scroll
    interval = 30
    for i in range(len(lst)):
        text = font.render(lst[i][1][1], True, (0, 0, 0))
        window.blit(text, (x, y))
        y += interval

def scrolling(scroll_speed, scroll, height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        scroll -= scroll_speed * 2
    if keys[pygame.K_DOWN]:
        scroll += scroll_speed * 2
    mouse = pygame.mouse.get_pos()
    if mouse[1] >= height - 50:
        scroll += scroll_speed * 2
    if mouse[1] <= 50:
        scroll -= scroll_speed * 2
    return scroll

def game(lst):
    pygame.init()
    width = 800
    height = 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SSBU Power Ranking")
    image = pygame.image.load("character_sprite/bayonetta.png")
    running = True
    scroll = 0
    scroll_speed = 10
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scroll = scrolling(scroll_speed, scroll, height)
        window.fill((255, 255, 255))
        window.blit(image, (0, 0))
        display_placement(lst, window, scroll)
        display_tag(lst, window, scroll)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()