import re
from turtle import distance, update
import pygame as pg
import math

pg.init()

# setting the window size
WIDTH, HEIGHT = 800, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)

FONT = pg.font.SysFont("comicsans", 16)


class Planet:
    # astronomical unit: approximately = the distance from the earth planet to the sun.
    AU = 149.6e6 * 1000
    # the Gravitational constant = the force of attraction between objects
    G = 6.67408e-11
    SCALE = 250 / AU  # 1AU ~= 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pg.draw.lines(win, self.color, False, updated_points, 2)

        pg.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)

            win.blit(distance_text, (x - distance_text.get_width() /
                                     2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        """
        calculate the force of attraction between two objects
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # if the other object is the sun then just get the distance
        if other.sun:
            self.distance_to_sun = distance

        force = (self.G * self.mass * other.mass) / (distance ** 2)
        # arc tangent of y over x distances
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        """
        update the position of the planet based on
        the force of attraction of every single other planet
        """
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # update the velocity of the planet by solving for acceleration using a = f / m (derived from Newton's second law)
        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        # acceleration cause velocity , velocity cause displacement
        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pg.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9722 * 10**24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.330 * 10**24)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)  # run the loop a max of 60 times per second
        WIN.fill((0, 0, 0))

        # when the user clicks the x button on the window the window will close
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pg.display.update()

    pg.quit()


main()
