import pygame

interval = 50

def load_images(lst):
    loaded_images = []
    x = 48
    for item in lst:
        try:
            image_path = f"PNG-128/{item[1][2]}-128.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (x, x / 1.5))
            loaded_images.append(image)
        except pygame.error:
            print(f"Unable to load the image {item[1][2]}.")
            loaded_images.append(None)
    return loaded_images

def load_character_images(lst):
    loaded_images = []
    x = 96
    for item in lst:
        try:
            image_path = f"character_sprite/{item[1][3][0]}.png"
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (x, x / 1.77))
            loaded_images.append(image)
        except pygame.error:
            print(f"Unable to load the image {item[1][3][0]}.")
            loaded_images.append(None)
    return loaded_images

def display_placement(lst, window, scroll):
    font = pygame.font.Font(None, 48)
    x = 0
    y = 20 - scroll
    for i in range(len(lst)):
        text = font.render(str(i + 1), True, (0, 0, 0))
        window.blit(text, (x, y))
        y += interval

def display_tag(lst, window, scroll):
    font = pygame.font.Font(None, 48)
    x = 80
    y = 20 - scroll
    for i in range(len(lst)):
        text = font.render(lst[i][1][1], True, (0, 0, 0))
        window.blit(text, (x, y))
        y += interval

def display_elo(lst, window, scroll):
    font = pygame.font.Font(None, 48)
    x = 400
    y = 20 - scroll
    for i in range(len(lst)):
        text = font.render(str(int(lst[i][1][0][0])), True, (0, 0, 0))
        window.blit(text, (x, y))
        y += interval

def display_flag(lst, window, scroll, loaded_images):
    x = 550
    y = 20 - scroll
    for i in range(len(lst)):
        image = loaded_images[i]
        if image is not None:
            window.blit(image, (x, y))
        y += interval

def display_character(lst, window, scroll, loaded_images):
    x = 625
    y = 20 - scroll - 10
    for i in range(len(lst)):
        image = loaded_images[i]
        if image is not None:
            window.blit(image, (x, y))
        y += interval

def scrolling(scroll_speed, scroll, height, length):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and scroll > 0:
        scroll -= scroll_speed * 2
    if keys[pygame.K_DOWN] and scroll < length * interval - height + 50:
        scroll += scroll_speed * 2
    mouse = pygame.mouse.get_pos()
    if mouse[1] >= height - 50 and scroll < length * interval - height + 50:
        scroll += scroll_speed * 2
    if mouse[1] <= 50 and scroll > 0:
        scroll -= scroll_speed * 2
    return scroll

def game(lst):
    pygame.init()
    width = 800
    height = 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SSBU Power Ranking")
    running = True
    scroll = 0
    scroll_speed = 10
    clock = pygame.time.Clock()
    loaded_flag_images = load_images(lst)
    loaded_character_images = load_character_images(lst)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scroll = scrolling(scroll_speed, scroll, height, len(lst))
        window.fill((255, 255, 255))
        display_placement(lst, window, scroll)
        display_tag(lst, window, scroll)
        display_elo(lst, window, scroll)
        display_flag(lst, window, scroll, loaded_flag_images)
        display_character(lst, window, scroll, loaded_character_images)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
