import pymunk

class circle:
    mass = 100
    radius = 0
    moment = None
    body = None
    shape = None

    def __init__(self, x, y, rad):
        self.mass = 100
        self.radius = rad
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.friction = 1
        self.shape.collision_type = 2