import pygame
import sys
from slider import Slider
from koch_snowflake import KochSnowflake

# Configuración inicial
WIDTH, HEIGHT = 1000, 700
FPS = 30
BACKGROUND_COLOR = (30, 30, 30)
MAX_DEPTH = 7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Copo de Nieve de Koch")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 14)

# Controles
sliders = [
    Slider(WIDTH//2 - 275, HEIGHT-200, 250, 10, 0, MAX_DEPTH, 0, "Nivel de Detalle"),
    Slider(WIDTH//2 + 25, HEIGHT-200, 250, 10, 1, 10, 1, "Grosor Linea"),
    Slider(100, HEIGHT-150, 250, 10, 0, 255, 0, "Linea R Ini"),
    Slider(100, HEIGHT-100, 250, 10, 0, 255, 0, "Linea G Ini"),
    Slider(100, HEIGHT-50, 250, 10, 0, 255, 0, "Linea B Ini"),
    Slider(400, HEIGHT-150, 250, 10, 0, 255, 0, "Linea R Fin"),
    Slider(400, HEIGHT-100, 250, 10, 0, 255, 0, "Linea G Fin"),
    Slider(400, HEIGHT-50, 250, 10, 0, 255, 0, "Linea B Fin"),
    Slider(700, HEIGHT-150, 250, 10, 0, 255, 0, "Relleno R"),
    Slider(700, HEIGHT-100, 250, 10, 0, 255, 0, "Relleno G"),
    Slider(700, HEIGHT-50, 250, 10, 0, 255, 0, "Relleno B"),
]

snowflake = KochSnowflake()
reset_button = pygame.Rect(WIDTH - 120, 20, 100, 30)

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for slider in sliders:
                    if slider.knob.collidepoint(event.pos):
                        slider.dragging = True
                if reset_button.collidepoint(event.pos):
                    snowflake.reset_view()
                    
            elif event.button == 3:
                snowflake.dragging = True
                snowflake.last_mouse = event.pos
                
            elif event.button == 4:
                snowflake.handle_zoom("in", event.pos)
                
            elif event.button == 5:
                snowflake.handle_zoom("out", event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for slider in sliders:
                    slider.dragging = False
            elif event.button == 3:
                snowflake.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if snowflake.dragging:
                dx = event.pos[0] - snowflake.last_mouse[0]
                dy = event.pos[1] - snowflake.last_mouse[1]
                snowflake.offset_x += dx
                snowflake.offset_y += dy
                snowflake.last_mouse = event.pos
                
            for slider in sliders:
                if slider.dragging:
                    slider.update(event.pos)

    # Actualizar parámetros
    depth = int(sliders[0].val)
    color_line1 = (int(sliders[2].val), int(sliders[3].val), int(sliders[4].val))
    color_line2 = (int(sliders[5].val), int(sliders[6].val), int(sliders[7].val))
    color_fill = (int(sliders[8].val), int(sliders[9].val), int(sliders[10].val))
    line_width = max(1, min(10, int(sliders[1].val)))
    
    # Generar y dibujar
    snowflake.generate(depth, color_line1, color_line2)
    snowflake.draw(screen, color_line1, color_line2, line_width, color_fill)
    
    # Dibujar controles
    for slider in sliders:
        slider.draw(screen)
    
    # Botón reset
    pygame.draw.rect(screen, (50, 150, 50), reset_button)
    reset_text = font.render("Reiniciar Vista", True, (255, 255, 255))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 5))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()