import pygame

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.knob = pygame.Rect(x, y - h, h*2, h*3)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.dragging = False
        self.label = label

    def draw(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.knob)
        
        font = pygame.font.SysFont('Arial', 14)
        label_text = font.render(f"{self.label}: {int(self.val)}", True, (255, 255, 255))
        surface.blit(label_text, (self.rect.x, self.rect.y - 30))

    def update(self, mouse_pos):
        if self.dragging:
            self.knob.centerx = max(self.rect.left, min(mouse_pos[0], self.rect.right))
            self.val = self.min + (self.knob.centerx - self.rect.left) / self.rect.width * (self.max - self.min)
            return True
        return False