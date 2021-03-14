# import the pygame module, so you can use it
import pygame
from railvoltagemonitor import RailVoltageMonitor
from server import CommandServer


# define a main function
def main():
    commandServer=CommandServer()
    # initialize the pygame module
    pygame.init()
    #pygame.joystick.init()

    #todo: see if the joystick is connected
    #joystick = pygame.joystick.Joystick(0)
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    #pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((800, 500))
    #pygame.draw.rect(screen,(0,0,205),pygame.Rect(100,100,50  ,50))
    # define a variable to control the main loop
    running = True
    left_track = 0
    right_track = 0
    left_channel = 0
    right_channel = 0
    # main loop
    while running:
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (0, 0, 205), (200, 100, 50, 200),1)
        pygame.draw.rect(screen, (0,0,205), (550,100,50,200),1)
        pygame.draw.rect(screen, (0,0,205), (125,350,200,50),1)
        pygame.draw.rect(screen, (0, 0, 205), (475, 350, 200, 50), 1)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.JOYAXISMOTION:
                pass
                # left_track = round(joystick.get_axis(1),2)
                # right_track = round(joystick.get_axis(4),2)
                # left_channel = round(joystick.get_axis(0),2)
                # right_channel = round(joystick.get_axis(3),2)

            if event.type == pygame.JOYBUTTONDOWN:
                pass
                # for i in range(joystick.get_numbuttons()):
                #     if(joystick.get_button(i)):
                #         print("state of button {} = {}".format(i,joystick.get_button(i)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    right_track = min(right_track + 10,127)
                    print(right_track)
                if event.key == pygame.K_DOWN:
                    right_track = max(right_track - 10,-127)
                if event.key == pygame.K_z:
                    left_track = max(left_track + 10,-127)
                if event.key == pygame.K_s:
                    left_track = max(left_track - 10,-127)
        commandServer.setServoChannel(9, left_track)
        commandServer.setServoChannel(8, right_track)
        commandServer.setServoChannel(3, left_channel)
        commandServer.setServoChannel(4, right_channel)
        draw_axis_horizontal(screen,200,100,200,50,left_track)
        draw_axis_horizontal(screen, 550, 100, 200, 50, right_track)
        draw_axis_vertical(screen,125,350,50,200,left_channel)
        draw_axis_vertical(screen, 475, 350, 50, 200, right_channel)
        pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)

def draw_axis_horizontal(screen,y,x,height,width,value):
    height_value = abs(value/100)*(height/2)
    if value==0: return
    if value<0:
        pygame.draw.rect(screen,(0,0,205),(y,x+((height/2)-height_value),width,height_value))
    else:
        pygame.draw.rect(screen,(0,0,205),(y,x+((height/2)),width,height_value))

def draw_axis_vertical(screen,y,x,height,width,value):
    width_value = abs(value/100)*(width/2)
    if value==0: return
    if value<0:
        pygame.draw.rect(screen,(0,0,205),(y+((width/2)-width_value),x,width_value,height))
    else:
        pygame.draw.rect(screen,(0,0,205),(y+((width/2)),x,width_value,height))

if __name__ == "__main__":
    # call the main function
    main()