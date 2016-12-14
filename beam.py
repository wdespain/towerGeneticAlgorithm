import math
import pymunk
import pygame

class beam:
    length = 60
    thickness = 3
    mass = 5
    moment = None
    body = None
    shape = None
    angle = 0
    beamID = -1
    previousPosition = []
    startingPosition = []

    def __init__(self, id, x, y, angle, length):
        self.length = length
        self.previousPosition = [x, y]
        self.startingPosition = [x, y]
        self.beamID = id
        self.angle = angle
        self.moment = pymunk.moment_for_segment(
            self.mass,
            (x, y),
            (int(x + (math.cos(math.radians(angle))*self.length)),
             int(y + (math.sin(math.radians(angle))*self.length))),
            self.thickness)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = x, y
        self.shape = pymunk.Segment(
            self.body,
            (x, y),
            (x + (math.cos(angle) * self.length), y + (math.sin(angle) * self.length)),
            self.thickness)
        self.shape.friction = 1
        self.shape.collision_type = 1

    def draw(self, screen):
        p = self.body.position.x, self.body.position.y
        pygame.draw.lines(screen, (0, 0, 255), False, p)