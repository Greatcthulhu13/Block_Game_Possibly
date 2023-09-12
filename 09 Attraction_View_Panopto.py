
import random
import pygame
import PyParticles

class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0
        
    def scroll(self, dx=0, dy=0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0


clock = pygame.time.Clock()

#set up the environment and the screen
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))

universe_screen = UniverseScreen(width, height)

pygame.display.set_caption('Space')

#create our environment
universe = PyParticles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])

#make the particles mass related to their appearance
def calculateRadius(mass):
    return mass ** (0.5)

#create 100 white particles
for p in range(100):
    particle_mass = random.randint(5,10)
    particle_size = calculateRadius(particle_mass)
    universe.addParticles(mass=particle_mass, size=particle_size, colour=(255,255,255))

running = True
#game loop
while running:
    
    #update the environment
    universe.update()
    screen.fill(universe.colour)

    particles_to_remove = []
    
    #go through and draw the particles on the screen after moving them
    for p in universe.particles:
        #if a collision has occured, we need to remove the particle
        if 'collide_with' in  p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collide_with']

        #adjust particle position based on view zoom and position
        mag = universe_screen.magnification
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * mag)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * mag)
        size = int(p.size * mag)
        
        if size < 2:
            pygame.draw.rect(screen, p.colour, (int(x), int(y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(x), int(y)), int(size), 0)

    #remove collided particles
            for p in particles_to_remove:
                if p in universe.particles:
                    universe.particles.remove(p)
            
    clock.tick(60)
    pygame.display.flip()

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universe_screen.scroll(dx=1)
            if event.key == pygame.K_RIGHT:
                universe_screen.scroll(dx=-1)
            if event.key == pygame.K_UP:
                universe_screen.scroll(dy=1)
            if event.key == pygame.K_DOWN:
                universe_screen.scroll(dy=-1)
            if event.key == pygame.K_EQUALS:
                universe_screen.zoom(2)
            if event.key == pygame.K_MINUS:
                universe_screen.zoom(0.5)
            if event.key == pygame.K_r:
                universe_screen.reset()
       