from random import *

from Data import Data
from Dot import Dot


class Population:

    def __init__(self, size: int) -> None:
        self.size: int = size
        self.dots: list["Dot"] = self.generate_pop(size)
        self.weights: list[float] = []
        self.best_dot_index: int = 0

    @staticmethod
    def generate_pop(size: int) -> list["Dot"]:
        dots = [Dot() for _ in range(size)]
        for dot in dots:
            dot.generate_genome()
        return dots

    def get_best_dot(self) -> None:
        self.best_dot_index = self.weights.index(max(self.weights))

    def get_weight(self) -> None:
        self.weights = [dot.fitness() for dot in self.dots]

    def evolve(self) -> None:

        new_gen: list["Dot"] = self.generate_pop(self.size)

        self.get_weight()
        self.get_best_dot()

        # elitism
        new_gen[0] = self.dots[self.best_dot_index].clone()

        # parent selection
        for i in range(1, self.size):
            new_gen[i] = self.select_parent().clone()

        # crossover
        new_gen = self.crossover_pop(new_gen)

        self.dots = new_gen

        self.reset_all()
        self.dots[0].color = "green"
        self.dots[0].radius = 4

    def select_parent(self) -> "Dot":
        """# by hand
        limit: float = random()*sum(self.weights)

        running_sum: float = 0.0
        for i, weight in enumerate(self.weights):
            running_sum += weight
            if running_sum > limit:
                return self.dots[i]

        # select only best dot
        # return self.dots[self.best_dot_index]"""

        # with random
        return choices(self.dots, weights=self.weights, k=1)[0]

    def reset_all(self):
        for dot in self.dots:
            dot.reset_dot()

    def crossover_pop(self, gen: list["Dot"]) -> list["Dot"]:
        for _ in range(self.size//2):
            if random() < Data.crossover_rate:
                # selection for crossover
                i1, i2 = randint(1, self.size-1), randint(1, self.size-1)

                gen[i1].genome, gen[i2].genome = self.crossover(gen[i1].genome, gen[i2].genome)

        return gen

    @staticmethod
    def crossover(genome1: list[int], genome2: list[int]) -> tuple[list[int], list[int]]:
        index = randint(1, Dot.genome_length)

        output1: list[int] = genome1[:index] + genome2[index:]
        output2: list[int] = genome2[:index] + genome1[index:]

        return output1, output2

    def mutate_all(self):
        for dot in self.dots[1:]:
            dot.mutate()

    def is_all_dead(self) -> bool:
        for dot in self.dots:
            if dot.alive:
                return False

        return True

    def __str__(self) -> str:
        return "\n".join([str(dot) for dot in self.dots])

    def __repr__(self):
        return str(self)
