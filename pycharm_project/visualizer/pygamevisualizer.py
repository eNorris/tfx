__author__ = 'Edward'

try:
    import pygame
    graphics = True
except ImportError:
    graphics = False


class Visualizer:

    def __init__(self):
        if not graphics:
            return
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
        if not graphics:
            return
        try:
            _ = iter(drawables)
        except TypeError:
            self.registerthis(drawables)
        else:
            for d in drawables:
                self.register(d)

    def registerthis(self, drawable):
        if not graphics:
            return
        self.drawables.add(drawable)
        drawable.visualizer = self
        #try:
        #    drawable.registervis()
        #except AttributeError:
        #    pass

    def unregister(self, drawables):
        if not graphics:
            return
        try:
            _ = iter(drawables)
        except TypeError:
            self.drawables.remove(drawables)
            drawables.visualizer = None
        else:
            for d in drawables:
                self.unregister(d)

    def screen_to_xy(self, screenx, screeny=None):
        if screeny is None:
            return (screenx[0] - self.gx) / self.scale, (-screenx[1] + 400 + self.gy) / self.scale
        else:
            return (screenx - self.gx) / self.scale, (-screeny + 400 + self.gy) / self.scale

    def xy_to_screen(self, x, y=None):
        if y is None:
            return self.scale * x[0] + self.gx, 400 + self.gy - self.scale * x[1]
        else:
            return self.scale * x + self.gx, 400 + self.gy - self.scale * y

    def xy_to_screen_px(self, x, y=None):
        if y is None:
            return int(self.scale * x[0] + self.gx), int(400 + self.gy - self.scale * x[1])
        else:
            return int(self.scale * x + self.gx), int(400 + self.gy - self.scale * y)

    def draw_all(self):
        self.screen.fill((220, 220, 220))
        surf = pygame.Surface((600, 400), pygame.SRCALPHA)
        pixarry = pygame.PixelArray(surf)
        #surfarry = pygame.surfarray.pixels2d(surf)  #pygame.surfarray.array2d(surf)

        for d in self.drawables:
            #print(d)
            left, right, bottom, top, zmin, zmax = d.get_bounds()
            lefti, topi = self.xy_to_screen_px(left, bottom)
            righti, bottomi = self.xy_to_screen_px(right, top)

            #print((righti-lefti, topi-bottomi))

            for i in range(max(0, lefti), min(righti+1, 599)):
                for j in range(max(0, bottomi), min(topi+1, 399)):
                    center = self.screen_to_xy(i + .5, j + .5)
                    #print("center = " + str(center))
                    if center in d:
                        #print("IN!")
                        pixarry[i][j] = d.fillcolor
                        #surfarry[i][j] = 234234  #d.fillcolor
                    else:
                        pixarry[i][j] = (0, 0, 0, 0)
                        #surfarry[i][j] = 0  #(0, 0, 0, 0)

        del pixarry

        self.screen.blit(surf, [0, 0], area=None, special_flags=0)
        #pygame.surfarray.blit_array(self.screen, surfarry)

        font = pygame.font.SysFont('Calibri', 15, True, False)
        sx, sy = self.screen_to_xy(pygame.mouse.get_pos())
        text = font.render(str(sx) + ", " + str(sy), True, (0, 0, 0))
        self.screen.blit(text, [0, 385])

        pygame.display.flip()

    def launch(self):
        if not graphics:
            return

        self.draw_all()

        pause_and_wait = True
        while pause_and_wait:
            #self.screen.fill((220, 220, 220))
            #for d in self.drawables:
            #    d.draw2d()
            self.draw_all()

            #font = pygame.font.SysFont('Calibri', 15, True, False)
            #sx, sy = self.screen_to_xy(pygame.mouse.get_pos())
            #text = font.render(str(sx) + ", " + str(sy), True, (0, 0, 0))
            #self.screen.blit(text, [0, 385])
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause_and_wait = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.active:
                        dx = pygame.mouse.get_pos()[0] - self.lx
                        dy = pygame.mouse.get_pos()[1] - self.ly
                        self.gx += dx
                        self.gy += dy
                    self.lx, self.ly = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button = event.button  # 1 = left, 2 = middle, 3 = right, 4 = wheel up, 5 = wheel down
                    if button == 1:
                        self.active = True
                    if button == 3:
                        foundone = False
                        for d in self.drawables:
                            if self.screen_to_xy(pygame.mouse.get_pos()) in d:
                                foundone = True
                                print(d)
                        if not foundone:
                            print("VOID")
                    if button in [4, 5]:
                        rx = self.gx - pygame.mouse.get_pos()[0]
                        ry = self.gy - (pygame.mouse.get_pos()[1] - 400)
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
                    #self.active = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.active = False
            #pygame.display.flip()