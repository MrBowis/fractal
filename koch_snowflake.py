import pygame
import math

WIDTH, HEIGHT = 1000, 800
INITIAL_SCALE = 1.0

class KochSnowflake:
    def __init__(self):
        self.points = []
        self.triangles = []
        self.vertices = []
        self.scale = INITIAL_SCALE
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse = (0, 0)

    def generate(self, depth, color1, color2):
        self.points = []
        self.triangles = []
        self.vertices = []
        center = (WIDTH/2 + self.offset_x, HEIGHT/2-100 + self.offset_y)
        size = min(WIDTH, HEIGHT) * 0.4 * self.scale
        
        # Triángulo equilátero inicial
        p1 = (center[0] - size/2, center[1] + size * math.sqrt(3)/6)
        p2 = (center[0] + size/2, center[1] + size * math.sqrt(3)/6)
        p3 = (center[0], center[1] - size * math.sqrt(3)/3)
        
        # Generar vértices para el relleno
        self._generate_vertices(p1, p2, depth, 0)
        self._generate_vertices(p2, p3, depth, 0)
        self._generate_vertices(p3, p1, depth, 0)
        
        # Generar segmentos y triángulos internos
        self._koch(p1, p2, depth, 0, color1, color2)
        self._koch(p2, p3, depth, 0, color1, color2)
        self._koch(p3, p1, depth, 0, color1, color2)

    def _generate_vertices(self, p1, p2, depth, current_depth):
        if current_depth == depth:
            self.vertices.extend([p1, p2])
            return
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        a = (p1[0] + dx/3, p1[1] + dy/3)
        b = (p1[0] + dx*2/3, p1[1] + dy*2/3)
        
        angle = math.radians(60)
        c = (
            a[0] + (b[0] - a[0]) * math.cos(angle) - (b[1] - a[1]) * math.sin(angle),
            a[1] + (b[0] - a[0]) * math.sin(angle) + (b[1] - a[1]) * math.cos(angle)
        )
        
        self._generate_vertices(p1, a, depth, current_depth + 1)
        self._generate_vertices(a, c, depth, current_depth + 1)
        self._generate_vertices(c, b, depth, current_depth + 1)
        self._generate_vertices(b, p2, depth, current_depth + 1)

    def _koch(self, p1, p2, depth, current_depth, color1, color2):
        if current_depth == depth:
            self.points.append((p1, p2))
            return
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        a = (p1[0] + dx/3, p1[1] + dy/3)
        b = (p1[0] + dx*2/3, p1[1] + dy*2/3)
        
        angle = math.radians(60)
        c = (
            a[0] + (b[0] - a[0]) * math.cos(angle) - (b[1] - a[1]) * math.sin(angle),
            a[1] + (b[0] - a[0]) * math.sin(angle) + (b[1] - a[1]) * math.cos(angle)
        )
        
        # Guardar triángulo interno con su profundidad
        self.triangles.append((a, c, b, current_depth))
        
        self._koch(p1, a, depth, current_depth + 1, color1, color2)
        self._koch(a, c, depth, current_depth + 1, color1, color2)
        self._koch(c, b, depth, current_depth + 1, color1, color2)
        self._koch(b, p2, depth, current_depth + 1, color1, color2)

    def draw(self, surface, color_line1, color_line2, line_width, color_fill):
        # Dibujar relleno principal
        if len(self.vertices) >= 3:
            pygame.draw.polygon(surface, color_fill, self.vertices)
        
        # Dibujar triángulos internos con el mismo color de relleno
        for triangle in self.triangles:
            a, c, b, depth = triangle
            pygame.draw.polygon(surface, color_fill, [a, c, b])
        
        # Dibujar bordes
        for i, (start, end) in enumerate(self.points):
            t = i / len(self.points)
            color = (
                color_line1[0] + (color_line2[0] - color_line1[0]) * t,
                color_line1[1] + (color_line2[1] - color_line1[1]) * t,
                color_line1[2] + (color_line2[2] - color_line1[2]) * t
            )
            pygame.draw.line(surface, color, start, end, line_width)

    def handle_zoom(self, direction, mouse_pos):
        zoom_factor = 1.1
        if direction == "in":
            self.scale *= zoom_factor
        else:
            self.scale /= zoom_factor
        
        self.offset_x += (mouse_pos[0] - WIDTH/2) * (1 - 1/zoom_factor if direction == "in" else zoom_factor - 1)
        self.offset_y += (mouse_pos[1] - HEIGHT/2) * (1 - 1/zoom_factor if direction == "in" else zoom_factor - 1)

    def reset_view(self):
        self.scale = INITIAL_SCALE
        self.offset_x = 0
        self.offset_y = 0