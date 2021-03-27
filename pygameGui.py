import pygame
from robot import TheBot,Robot

class Gui(object):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.window = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Wall-e controller software")
        self.screen = pygame.display.get_surface()
        self.state = "awaiting connection"
        self.is_joystick_connected = pygame.joystick.get_count() > 0

        if self.is_joystick_connected:
            self.joystick = pygame.joystick.Joystick(0)

    def start(self):
        running = True
        while(running):

            if self.state == "awaiting connection":
                if TheBot.is_connected:
                    self.state = "connected"
                    continue
                self.connectionScreen()
                print("awaiting connection")
            elif self.state == "connected":
                self.mainScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.JOYAXISMOTION:
                    #TheBot.absolute_move_track(Robot.LEFT_TRACK,round((self.joystick.get_axis(1)*128)+128))
                    #TheBot.absolute_move_track(Robot.RIGHT_TRACK, round((self.joystick.get_axis(3) * 128) + 128))
                    TheBot.absolute_move_part(Robot.HEAD_ROTATION,round((self.joystick.get_axis(2) * 128) + 128))
                    TheBot.absolute_move_part(Robot.NECK_HEIGHT, round((self.joystick.get_axis(3) * 128) + 128))
                    TheBot.absolute_move_part(Robot.NECK_TILT, round((self.joystick.get_axis(1) * 128) + 128))
                    #                 right_track = round(joystick.get_axis(4),2)
                    #                 left_channel = round(joystick.get_axis(0),2)
                    #                 right_channel = round(joystick.get_axis(3),2)
            pygame.display.flip()

    def connectionScreen(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((255,255,255))
        font = pygame.font.Font(None,36)
        text = font.render("Test tekst",True,(0,0,0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text,textpos)


    def mainScreen(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, (0, 0, 205), (200, 100, 50, 200),1)