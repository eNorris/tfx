__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False


class Visualizer:

    def __init__(self):
        if not graphics: return
        pygame.init()

        self.screen_size = (600, 400)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill((220, 220, 220))

        pygame.display.set_caption("Meshing Visualizer v1.0")

        self.clock = pygame.time.Clock()
        self.drawables = set()

        self.gx, self.gy = 300, -200
        self.scale = 1.0
        self.lx, self.ly = 0, 0
        self.active = False

    def register(self, drawables):
        if not graphics: return
        try:
            _ = iter(drawables)
        except TypeError:
            self.drawables.add(drawables)
            drawables.visualizer = self
        else:
            for d in drawables:
                self.register(d)

    def registerthis(self, drawable):
        if not graphics: return
        self.drawables.add(drawable)
        drawable.visualizer = self

    def unregister(self, drawables):
        if not graphics: return
        try:
            _ = iter(drawables)
        except TypeError:
            self.drawables.remove(drawables)
            drawables.visualizer = None
        else:
            for d in drawables:
                self.unregister(d)

    def launch(self):
        if not graphics: return
        #b = Box2d.Box2d((0, 0), (12, 0), (0, 12))
        #print(str(b))
        #b.set_pos((50, 50))
        #self.register(b)

        for d in self.drawables:
            d.draw2d()
        pygame.display.flip()

        pause_and_wait = True
        #time = 2
        while pause_and_wait:
            #b.rotate_about(-.01, (100, -time))
            #time += 5
            #b.translate([0, 3])
            #print(b)
            self.screen.fill((220, 220, 220))
            for d in self.drawables:
                d.draw2d()

            font = pygame.font.SysFont('Calibri', 15, True, False)
            text = font.render(
                str((pygame.mouse.get_pos()[0] - self.gx) / self.scale) + \
                ", " + str(-(pygame.mouse.get_pos()[1]-400 - self.gy) / self.scale),
                True, (0, 0, 0))
            self.screen.blit(text, [0, 385])
            #pygame.draw.rect(b.visualizer.screen, (220, 220, 220), [0, 0, 100, 600], 0)
            #b.draw2d()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause_and_wait = False
                elif event.type == pygame.MOUSEMOTION:
                    #print("MOVE")
                    if self.active:
                        dx = pygame.mouse.get_pos()[0] - self.lx
                        dy = pygame.mouse.get_pos()[1] - self.ly
                        #dx *= self.scale
                        #dy *= self.scale
                        self.gx += dx
                        self.gy += dy
                    self.lx, self.ly = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button = event.button  # 1 = left, 2 = middle, 3 = right, 4 = wheel up, 5 = wheel down
                    if button in [4, 5]:
                        rx = self.gx - pygame.mouse.get_pos()[0]
                        ry = self.gy - (pygame.mouse.get_pos()[1] - 400)
                        #print(pygame.mouse.get_pos())
                        rxnew, rynew = 0, 0
                        if button == 4:
                            self.scale *= 1.2
                            rxnew = rx * 1.2
                            rynew = ry * 1.2
                        if button == 5:
                            self.scale /= 1.2
                            rxnew = rx / 1.2
                            rynew = ry / 1.2
                        self.gx = self.gx - rx + rxnew
                        self.gy = self.gy - ry + rynew
                    #print("scale = " + str(self.scale))
                    #print("ACTIVE")
                    #print(event.button)
                    #print(pygame.mouse.get_pressed())
                    self.active = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    #print("INACTIVE")
                    self.active = False
            pygame.display.flip()