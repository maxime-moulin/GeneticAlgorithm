# import the pygame module
import pygame
import time
from Population import Population
from Data import Data

# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *


# initialize pygame
class Main:
    # Define the dimensions of screen object
    Data.screen = pygame.display.set_mode(Data.dimensions)

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Genetic Algorithm")
        self.background: "pygame.rect" = Data.screen.get_rect()

        self.population: "Population" = Population(500)

        # Variable to keep our game loop running
        self.running: bool = True

        self.loop()

    def update(self) -> None:
        for dot in self.population.dots:
            dot.move()

            pygame.draw.circle(Data.screen, dot.color, dot.center, dot.radius)

    def loop(self):
        # Our game loop
        while self.running:
            pygame.draw.rect(Data.screen, "white", self.background)
            pygame.draw.circle(Data.screen, "red", (Data.width / 2, 15), 5)

            self.update()

            pygame.display.flip()

            if self.population.is_all_dead():
                self.population.evolve()
                self.population.mutate_all()

            # for loop through the event queue
            for event in pygame.event.get():

                # Check for QUIT event
                if event.type == QUIT:
                    self.running = False
                    print(self.population.dots[self.population.best_dot_index])

            time.sleep(0.02)


main = Main()
