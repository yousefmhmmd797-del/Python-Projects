import pygame

pygame.init()
window = pygame.display.set_mode((400,500))
clock = pygame.time.Clock()
test_surface = pygame.surface((100,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.Quit:
            pygame.Quit()
    window.fill((175,215,70))
    window.blit(test_surface, (200,500))
    pygame.display.update()
    clock.tikc(60)