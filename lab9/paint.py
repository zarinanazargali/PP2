import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Advanced Drawing App")

    radius = 15
    mode = 'pen'
    color = (0, 0, 255)
    drawing = False
    start_pos = None
    points = []

    def drawLineBetween(screen, start, end, width, color):
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))
        for i in range(iterations):
            progress = i / iterations
            x = int(start[0] * (1 - progress) + end[0] * progress)
            y = int(start[1] * (1 - progress) + end[1] * progress)
            pygame.draw.circle(screen, color, (x, y), width)

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_p:
                    mode = 'pen'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'right_triangle'
                elif event.key == pygame.K_y:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    mode = 'rhombus'
                elif event.key == pygame.K_1:
                    color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)
                elif event.key == pygame.K_4:
                    color = (255, 255, 0)
                elif event.key == pygame.K_5:
                    color = (255, 170, 200)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    points = [event.pos]
                elif event.button == 3:
                    radius = max(1, radius - 1)
                elif event.button == 2:
                    radius = min(200, radius + 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    if mode == 'rect':
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(screen, color, rect, 2)
                    elif mode == 'circle':
                        radius_circle = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(screen, color, start_pos, radius_circle, 2)
                    elif mode == 'square':
                        size = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                        rect = pygame.Rect(start_pos, (size, size))
                        pygame.draw.rect(screen, color, rect, 2)
                    elif mode == 'right_triangle':
                        points_tri = [start_pos, (start_pos[0], end_pos[1]), (end_pos[0], end_pos[1])]
                        pygame.draw.polygon(screen, color, points_tri, 2)
                    elif mode == 'equilateral_triangle':
                        dx = end_pos[0] - start_pos[0]
                        p1 = start_pos
                        p2 = (start_pos[0] - dx, end_pos[1])
                        p3 = (start_pos[0] + dx, end_pos[1])
                        pygame.draw.polygon(screen, color, [p1, p2, p3], 2)
                    elif mode == 'rhombus':
                        mx = (start_pos[0] + end_pos[0]) // 2
                        my = (start_pos[1] + end_pos[1]) // 2
                        points_rhomb = [
                            (mx, start_pos[1]),
                            (end_pos[0], my),
                            (mx, end_pos[1]),
                            (start_pos[0], my)
                        ]
                        pygame.draw.polygon(screen, color, points_rhomb, 2)
                    start_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                pos = event.pos
                if mode == 'pen':
                    drawLineBetween(screen, points[-1], pos, radius, color)
                    points.append(pos)
                elif mode == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), pos, radius)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
