# Matthew
# March 2024
# Angry Birds Simulation (Course Project)

import pygame, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode
import math

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

def load_image(name):
    image = pygame.image.load(name)
    return image

class MyCircle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(self.image, color, (width//2, height//2), cx, cy)
        self.rect = self.image.get_rect()

    def update(self):
        pass

class MyRect(pygame.sprite.Sprite):
    def __init__(self, color, width, height, alpha=255):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect)

        self.picked = False

    def set_pos(self, pos):
        self.rect.x = pos[0] - self.rect.width//2
        self.rect.y = pos[1] - self.rect.height//2

    def update(self):
        pass

class MyText():
    def __init__(self, color, background=WHITE, antialias=True, fontname="comicsansms", fontsize=16):
        pygame.font.init()
        self.font = pygame.font.SysFont(fontname, fontsize)
        self.color = color
        self.background = background
        self.antialias = antialias
    
    def draw(self, str1, screen, pos):
        text = self.font.render(str1, self.antialias, self.color, self.background)
        screen.blit(text, pos)



class Simulation:
    def __init__(self):
        # TODO
        self.gamma = 0.0001 # friction
        self.mass1 = 1.0 # mass of bird
        self.t = 0
        self.gravity = 9.8

        self.dt = 0.033 # 33 millisecond, which corresponds to 30 fps
        self.state1 = np.zeros(4, dtype='float32') #stores x, y, vx, vy for mass 1
        self.cur_time = 0

        self.k1 = 120 # spring constant
        self.l1 = 10 # length of spring
        self.c1 = 0.5

        
        self.paused = True # starting in paused mode

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_f_params(self.gamma, self.gravity)

    def f(self, t, state, arg1, arg2):
        # TO DO

        #dx = (self.vx * self.dt)
        #dy = (self.vy * self.dt)
        #dvx = ((-(self.gamma * self.vx)/self.mass) * self.dt)
        #dvy = ((-(self.gravity + (self.gamma * self.vy))) / self.mass)
        #force = 
        
        #dstate = np.array()

        pass
        
    def setup(self, pos, speed, angle_degrees):
    #def setup(self, pos, speed):
        # TO DO

        # take the argument degrees and convert into radians
        angle_radians = angle_degrees * (3.1415/180)

        #calculate x and y vel components

        self.x = pos[0]
        self.vx = speed * np.cos(angle_radians)
        self.y = pos[1]
        self.vy = speed * np.sin(angle_radians)


        self.times = [self.cur_time*1000]
        self.pos = [self.x, self.y]
        self.velocities = [self.vx, self.vy]

        #self.solver.set_initial_value([self.pos[0], self.pos[1], dx, dy], self.cur_time)
        
        self.trace_x = [self.pos[0]]
        self.trace_y = [self.pos[1]]


        self.angle_radians = math.atan2(self.y, self.x) #in radians
        self.angle1 = math.degrees(self.angle_radians) #in degrees

        self.cur_length1 =  np.linalg.norm(self.pos)
        self.deformation1 = self.cur_length1 - self.l1

        #conservation of energy (calculate velocity of bird when it leaves the spring, when spring is released)
        #displaying values to check them manually for correctness
        print("spring constant: k = ", self.k1)
        print("mass: m = ", self.mass1)
        print("length of compressed spring: cur_length1 = ", self.cur_length1)
        print("deformation: si = ", self.deformation1)
        print("angle1 (degrees) = ", self.angle1)

        self.vf = np.absolute(np.sqrt(self.k1 / self.mass1) * (self.deformation1))
        print("speed = ", self.vf)


    def step(self):
        self.cur_time += self.dt

        # TODO
        self.x += self.vx * self.dt
        self.vx += (self.dt * (-(self.gamma * self.vx) / self.mass1)) # Velocity

        self.y += self.vy * self.dt
        self.vy += (self.dt * (-(self.gravity + self.gamma * self.vy) / self.mass1))

        self.pos = [self.x, self.y]

        self.trace_x.append(self.pos[0])
        self.trace_y.append(self.pos[1])

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

def sim_to_screen(win_height, x, y):
    '''flipping y, since we want our y to increase as we move up'''
    x += 10
    y += 10

    return x, win_height - y

def main():

    # initializing pygame
    pygame.init()

    text = MyText(BLACK)

    # top left corner is (0,0)
    win_width = 640
    win_height = 480
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('2D projectile motion')

    # setting up a sprite group, which will be drawn on the screen

    my_sprite1 = MyCircle(RED, 10, 10) #create red bird
    my_group = pygame.sprite.Group(my_sprite1)

    #added this for pig
    my_sprite2 = MyCircle(GREEN, 10, 10) #create green pig
    my_group2 = pygame.sprite.Group()
    my_sprite2.rect.x = 300
    my_sprite2.rect.y = 470

    my_group2.add(my_sprite2) #add pig to screen

    # setting up simulation
    sim = Simulation()

    #angle_degrees = math.degrees(sim.angleoftriangle)


    #input initial values here
    sim.setup([3.65, 3.65], 53, 45) # position, speed, angle

    print('--------------------------------')
    print('Usage:')
    print('Press (r) to start/resume simulation')
    print('Press (p) to pause simulation')
    print('Press (space) to step forward simulation when paused')
    print('--------------------------------')

    print("velocity when bird leaves the spring: vf = ", sim.vf)

    while True:
        # 30 fps
        clock.tick(60)

        # update sprite x, y position using values
        # returned from the simulation
        my_sprite1.rect.x, my_sprite1.rect.y = sim_to_screen(win_height, sim.pos[0], sim.pos[1])

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            sim.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            sim.resume()
            continue
        else:
            pass
        

        # clear the background, and draw the sprites
        screen.fill(WHITE)
        my_group.update()
        my_group.draw(screen)

        #for pig
        my_group2.update()
        my_group2.draw(screen)
        text.draw("Angry Birds (Simplified Edition)", screen, (10,10))
        pygame.display.flip()

        if sim.pos[1] <= 0.:
            pygame.quit()
            break

        # update simulation
        if not sim.paused:
            sim.step()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim.step()

    plt.figure(1)
    plt.plot(sim.trace_x, sim.trace_y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.title('2D Projectile Trajectory of the Bird')
    plt.show()


if __name__ == '__main__':
    main()