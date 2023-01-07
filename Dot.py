from pygame.math import Vector2
from random import*
from Data import Data


class Dot:
    genome_length = 500

    def __init__(self) -> None:
        self.vel: "Vector2" = Vector2(0, 0)
        self.acc: "Vector2" = Vector2(1, 0)

        self.genome: list[int] = []

        self.center: "Vector2" = Vector2(Data.width//2, Data.height - 10)
        self.step: int = 0
        self.alive: bool = True
        self.color = "black"
        self.radius = 2
        self.goal_reached: bool = False

    def reset_dot(self):
        self.center = Vector2(Data.width // 2, Data.height - 10)
        self.step = 0
        self.alive = True
        self.color = "black"
        self.radius = 2
        self.vel = Vector2(0, 0)
        self.acc = Vector2(1, 0)
        self.goal_reached = False

    def generate_genome(self) -> None:
        self.genome = [randrange(360) for _ in range(self.genome_length)]

    def mutate(self) -> None:
        for i in range(len(self.genome)):
            if random() < Data.mutation_rate:
                self.genome[i] = randrange(360)

    def move(self) -> None:
        if self.alive:
            if len(self.genome) > self.step:
                self.acc = Vector2(1, 0)
                self.acc = Vector2.rotate(self.acc, self.genome[self.step])
                self.acc.normalize()
                self.step += 1
                self.vel += self.acc
                if self.vel.length() > 5.0:
                    self.vel.scale_to_length(5.0)

                self.center += self.vel

                if not (2 < self.center.x < Data.width-2)\
                        or not (2 < self.center.y < Data.height-2)\
                        or self.is_goal_reached():
                    self.alive = False
            else:
                self.alive = False

    def is_goal_reached(self) -> bool:
        self.distance_to_goal()
        return self.goal_reached

    def distance_to_goal(self) -> float:
        distance = Vector2.length(self.center - Vector2(Data.width//2, 15)) - 5
        if distance <= 0.0:
            self.goal_reached = True
            return 0.1
        return distance

    def fitness(self) -> float:
        if self.goal_reached:
            return 1.0/16.0 + 10000.0 / (self.step**2)
        return 1.0 / (self.distance_to_goal()**2)

    def clone(self) -> "Dot":
        new_dot: "Dot" = Dot()
        new_dot.genome = self.genome.copy()
        return new_dot

    def __str__(self) -> str:
        return f"fitness = {self.fitness()} \ngenome = {self.genome} \n"

    def __repr__(self) -> str:
        return str(self)
